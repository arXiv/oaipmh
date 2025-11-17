from typing import Dict, Optional, Union, List, Tuple
from datetime import datetime, timezone

from flask import render_template

from arxiv.db.models import Metadata
from arxiv.integration.fastly.headers import add_surrogate_key
from arxiv.taxonomy.category import Group, Archive, Category
from arxiv.taxonomy.definitions import CATEGORIES

from oaipmh.processors.db import get_list_data

from oaipmh.data.oai_errors import OAINoRecordsMatch
from oaipmh.data.oai_config import RECORDS_LIMIT, IDENTIFIERS_LIMIT
from oaipmh.data.oai_properties import OAIParams, MetadataFormat
from oaipmh.processors.resume import ResToken
from oaipmh.requests.param_processing import create_oai_id
from oaipmh.serializers.create_records import arXivOldRecord, arXivRawRecord, arXivRecord, dcRecord, Header, Record
from oaipmh.serializers.output_formats import Response

def fetch_list(just_ids:bool, start_date :datetime, end_date:datetime, meta_type:MetadataFormat, rq_set:Optional[Union[Group, Archive, Category]], skip: int, query_data: Dict[OAIParams, str])-> Response:
    """fetches the required data for a record for a specific format 
    dates are in UTC, as is the data in the database columns being queried
    converts data into specific format and renders record template
    """
 
    all_versions = False if just_ids else meta_type.all_versions
    limit = IDENTIFIERS_LIMIT if just_ids else RECORDS_LIMIT

    data=get_list_data(just_ids, start_date, end_date, all_versions, rq_set, skip, limit)
    if not data:
        raise OAINoRecordsMatch(query_params=query_data)
    
    last_paper, last_datetime=find_last_result(data)
    objects=create_records(data, just_ids, meta_type)
    objects.sort()

    #resumption tokens
    res_token=None
    if OAIParams.RES_TOKEN in query_data: #need to have either a new resumption token or an empty one
        res_token=ResToken({},0, True)

    #create resumption token if more results than limit
    if len(objects)>limit: 
        last_date=last_datetime.date()
        first_date= objects[0].date.date() if just_ids else objects[0].header.date.date()

        if last_date== first_date: #all the same day
            res_token=ResToken(query_data, skip+limit)

        else: #resume from final day
            #count how many entries from the last day are being displayed
            to_skip=-1 #we are already dropping the one over the limit
            for obj in reversed(objects): 
                compare_date = obj.date.date() if just_ids else obj.header.date.date()
                if compare_date != last_date:  # Stop when reaching a different date
                    break
                to_skip += 1  

            #create the new query
            new_query=query_data
            new_query[OAIParams.FROM]=last_date.strftime('%Y-%m-%d')
            res_token=ResToken(new_query, to_skip)

        #remove the extra object above limit
        objects = [item for item in objects if (item.id if just_ids else item.header.id) != last_paper]

    now=datetime.now(timezone.utc)
    if just_ids:
        response=render_template("list_identifiers.xml", 
            response_date=now,
            query_params=query_data,
            headers=objects,
            token=res_token
            )
    else:
        response=render_template("list_records.xml", 
            response_date=now,
            query_params=query_data,
            records=objects,
            format=meta_type.prefix,
            token=res_token
            )
    
    if end_date>= now:
        headers={'Surrogate-Control': f'max-age=3600'} #this data is still changing
    else:
        headers={'Surrogate-Control': f'max-age=345600'} #gets cleared by announce
    headers=add_surrogate_key(headers,["announce", "oai-list"])        
              
    return response, 200, headers

def find_last_result(data: List[Metadata])->Tuple[str, datetime]:
    """finds the paper that would have been the last selected document from the database query.
    Final paper is dropped if limit is exceeded. Selection is done at this point before dates can be assigned from other columns like created
    """
    last_modtime=0
    latest_paper=""
    for item in data:
        if item.is_current and item.modtime >= last_modtime:
            if item.modtime > last_modtime:
                last_modtime=item.modtime
                latest_paper=item.paper_id
            else: #if they are equal timestamps
                if latest_paper < item.paper_id:
                    last_modtime=item.modtime
                    latest_paper=item.paper_id
    
    last_date=datetime.fromtimestamp(last_modtime, tz=timezone.utc)
    return create_oai_id(latest_paper), last_date

def create_records(data: List[Metadata], just_ids:bool, format:MetadataFormat)->List[Union[Header, Record]]:
    """turns data from the database into header or Record objects"""
    items=[]
    if just_ids:
        for item in data:
            categories: List[Category]=[]
            if item.abs_categories:
                for cat in item.abs_categories.split():
                    categories.append(CATEGORIES[cat])
            header=Header(item.paper_id, datetime.fromtimestamp(item.modtime, tz=timezone.utc), categories)
            items.append(header)
    else: 
        if format.prefix=="arXiv":
            for item in data:
                items.append(arXivRecord(item))
        elif format.prefix=="arXivOld":
            for item in data:
                items.append(arXivOldRecord(item))
        else: #these two can (should) have multiple entries for the same paper
            current_id=None
            current_group = []
            for item in data:
                if item.paper_id != current_id:
                    if current_group: #process last paper
                        if format.prefix=="arXivRaw":
                            items.append(arXivRawRecord(current_group))
                        else:
                            items.append(dcRecord(current_group))
                    current_id = item.paper_id
                    current_group = [item]
                else:
                    current_group.append(item)
            
            #process last group
            if format.prefix=="arXivRaw":
                items.append(arXivRawRecord(current_group))
            else:
                items.append(dcRecord(current_group))

    return items

