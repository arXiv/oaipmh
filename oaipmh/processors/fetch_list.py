from typing import Dict, Optional, Union, List
from datetime import datetime, timezone

from flask import render_template

from arxiv.db.models import Metadata
from arxiv.taxonomy.category import Group, Archive, Category

from oaipmh.processors.db import get_list_data

from oaipmh.data.oai_errors import OAINoRecordsMatch
from oaipmh.data.oai_config import RECORDS_LIMIT, IDENTIFIERS_LIMIT
from oaipmh.data.oai_properties import OAIParams, MetadataFormat
from oaipmh.processors.resume import ResToken
from oaipmh.serializers.create_records import arXivOldRecord, arXivRawRecord, arXivRecord, dcRecord, Header, Record
from oaipmh.serializers.output_formats import Response

def fetch_list(just_ids:bool, start_date :datetime, end_date:datetime, meta_type:MetadataFormat, rq_set:Optional[Union[Group, Archive, Category]], skip: int, query_data: Dict[OAIParams, str])-> Response:
    """fetches the required data for a record for a specific format 
    converts data into specific format and renders record template
    """
 
    all_versions = False if just_ids else meta_type.all_versions
    limit = IDENTIFIERS_LIMIT if just_ids else RECORDS_LIMIT
    limit=5 #TODO remove
    #TODO category processing

    data=get_list_data(just_ids, start_date, end_date, all_versions, None, skip, limit)
    if not data:
        raise OAINoRecordsMatch(query_params=query_data)
    
    objects=create_records(data, just_ids, meta_type)

    #resumption token handling
    if len(objects)>limit: 
        last_date=objects[-1].date.date()
        if last_date== objects[0].date.date(): #all the same day
            objects.pop() #remove the extra item
            res_token=ResToken(query_data, skip+limit) 
        else: #resume from final day
            to_skip=0
            for i in range(len(objects) - 1, -1, -1):  # iterate backward through list
                to_skip+=1
                if objects[i].date.date() != last_date:
                    new_query=query_data
                    new_query[OAIParams.FROM]=last_date.strftime('%Y-%m-%d')
                    res_token=ResToken(new_query, to_skip)
                    break
    else:
        res_token=None

    response='' #TODO rendering
    headers={"Content-Type":"application/xml"}
    return response, 200, headers

def create_records(data: List[Metadata], just_ids:bool, format:MetadataFormat)->List[Union[Header, Record]]:
    """turns data from the database into header or Record objects and sorts them"""
    items=[]
    if just_ids:
        for item in data:
            header=Header(item.paper_id, datetime.fromtimestamp(item.modtime, tz=timezone.utc), item.abs_categories)
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

    items.sort()
    return items

