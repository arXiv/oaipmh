from typing import Optional, List, Union, Tuple, Set
from datetime import datetime

from sqlalchemy import  or_, and_
from sqlalchemy.orm import aliased, load_only

from arxiv.db import Session
from arxiv.db.models import Metadata, t_arXiv_in_category
from arxiv.identifier import Identifier
from arxiv.taxonomy.category import Group, Archive, Category

def get_record_data(arxiv_id: Identifier, all_versions:bool )-> Optional[Union[Metadata, List[Metadata]]]:
    """fetch metadata for a specific paper"""
    data_subquery = (
        Session.query(Metadata)
        .filter(Metadata.paper_id == arxiv_id.id)
        .subquery()
    )

    metadata_alias = aliased(Metadata, data_subquery)
    if all_versions:
        result = Session.query(metadata_alias).all()
    else:
        result = (
            Session.query(metadata_alias)
            .filter(metadata_alias.is_current == 1)
            .first()
        )
    return result

def get_list_data(just_ids:bool, start_date :datetime, end_date:datetime, all_versions: bool, rq_set:Optional[Union[Group, Archive, Category]], skip:int, limit: int)->List[Metadata]:
    """fetches list of data according to given parameters"""
    #updated is sometimes NULL so we are using modtime
    start_timestamp=start_date.timestamp()
    end_timestamp=end_date.timestamp()

    #all papers that have been updated within the time frame
    doc_ids=( 
        Session.query(Metadata.document_id)
        .filter(
            Metadata.modtime >= start_timestamp,  
            Metadata.modtime <= end_timestamp,  
            Metadata.is_current == 1,  
        )
        .subquery()
    )

    #filter for certain categories
    if rq_set:
        archives, cats=process_requested_subject(rq_set)
        aic = aliased(t_arXiv_in_category)
        cat_conditions = [and_(aic.c.archive == arch_part, aic.c.subject_class == subj_part) for arch_part, subj_part in cats]
        doc_ids=(Session.query(doc_ids.c.document_id)
            .join(aic, doc_ids.c.document_id == aic.c.document_id)
            .filter(
                or_(
                    aic.c.archive.in_(archives),
                    or_(*cat_conditions),
                )
            )
            .subquery()
        )   
    
    #select exact group of documents that will be reported on
    selected_doc_ids=(
        Session.query(Metadata.document_id)
        .filter(Metadata.document_id.in_(doc_ids.select()))
        .filter(Metadata.is_current == 1)
        .order_by(Metadata.modtime, Metadata.paper_id)
        .offset(skip)
        .limit(limit+1) #one extra to see if resumption token needed
        .subquery()
    )

    #fetch the metadata
    if just_ids: #only need the data for the header portion
        data = (
            Session.query(Metadata)
            .filter(Metadata.document_id.in_(selected_doc_ids.select()), 
                    Metadata.is_current == 1
            )
            .options(load_only(
                Metadata.paper_id,
                Metadata.abs_categories,
                Metadata.is_current,
                Metadata.modtime
            ))
            .all()   
        )
    else: #for listing records instead of just header
        if all_versions: #some formats require all versions
            data = (
                Session.query(Metadata)
                .filter(Metadata.document_id.in_(selected_doc_ids.select()))
                .order_by(Metadata.paper_id)
                .all()  
            )
        else:
            data = (
                Session.query(Metadata)
                .filter(Metadata.document_id.in_(selected_doc_ids.select()), 
                        Metadata.is_current == 1
                )
                .all()   
            )

    return data

def process_requested_subject(subject: Union[Group, Archive, Category])-> Tuple[Set[str], Set[Tuple[str,str]]]:
    """ 
    set of archives to search if appliable, 
    set of tuples are the categories to check for in addition to the archive broken into archive and category parts
    only categories not contained by the set of archives will be returned seperately to work with the archive in category table
    """
    archs=set()
    cats=set()

    #utility function
    def process_cat_name(name: str) -> None:
        #splits category name into parts and adds it
        if "." in name:
            arch_part, cat_part = name.split(".")
            if arch_part not in archs:
                cats.add((arch_part, cat_part))
        elif name not in archs:
            archs.add(name)

    #handle category request
    if isinstance(subject, Category):
        process_cat_name(subject.id)
        if subject.alt_name:
            process_cat_name(subject.alt_name)

    elif isinstance(subject, Archive):
        archs.add(subject.id)
        for category in subject.get_categories(True):
            process_cat_name(category.alt_name) if category.alt_name else None 

    elif isinstance(subject, Group):
        for arch in subject.get_archives(True):
            archs.add(arch.id)
        for arch in subject.get_archives(True): #twice to avoid adding categories covered by archives
            for category in arch.get_categories(True):
                process_cat_name(category.alt_name) if category.alt_name else None 

    return archs, cats

def check_paper_existence(paper_id: Identifier) ->bool:
    #true if paper exists, false otherwise
    result=Session.query(Metadata.document_id).filter(Metadata.paper_id==paper_id.id).first()
    return bool(result)
