from typing import Optional, List, Union
from datetime import datetime
from sqlalchemy.orm import aliased, load_only

from arxiv.db import Session
from arxiv.db.models import Metadata
from arxiv.identifier import Identifier

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

def get_list_data(just_ids:bool, start_date :datetime, end_date:datetime, all_versions: bool, cat_data, skip:int, limit: int)->List[Metadata]:
    """fetches list of data according to given parameters"""
    #updated is sometimes NULL so we are using modtime
    start_timestamp=start_date.timestamp()
    end_timestamp=end_date.timestamp()

    limit=10 #TODO remove
    #all papers that have been updated within the time frame
    doc_ids=( 
        Session.query(Metadata.document_id) #TODO may want to fetch more because im going to need it anyways
        .filter(
            Metadata.modtime >= start_timestamp,  
            Metadata.modtime <= end_timestamp,  
            Metadata.is_current == 1,  
        )
        .subquery()
    )

    #filter for certain categories
    if cat_data:
        #TODO filter and reset doc_ids
        pass
    
    #select exact group of documents that will be reported on
    selected_doc_ids=(
        Session.query(Metadata.document_id)
        .filter(Metadata.document_id.in_(doc_ids.select()))
        .filter(Metadata.is_current == 1)
        .order_by(Metadata.modtime, Metadata.paper_id)
        .offset(skip)
        .limit(limit+1) #to see if we need a resumtion token
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
                Metadata.modtime
            ))
            .order_by(Metadata.paper_id)
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
                .order_by(Metadata.paper_id)
                .all()   
            )

    return data

