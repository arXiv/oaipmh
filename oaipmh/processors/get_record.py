from typing import Dict
from datetime import datetime, timezone

from flask import render_template

from arxiv.identifier import Identifier

from oaipmh.processors.db import get_record_data_all, get_record_data_current
from oaipmh.data.oai_errors import OAINonexistentID
from oaipmh.data.oai_properties import OAIParams, MetadataFormat
from oaipmh.serializers.create_records import arXivOldRecord, arXivRawRecord, arXivRecord, dcRecord
from oaipmh.serializers.output_formats import Response

def do_get_record(arxiv_id: Identifier, format: MetadataFormat, query_data: Dict[OAIParams, str])-> Response:
    """fetches the required data for a record for a specific format 
    converts data into specif format and renders record template
    """
    if format.all_versions:
        data=get_record_data_all(arxiv_id)
        if not data: 
            raise OAINonexistentID("Nothing found for this ID",query_params=query_data)
        
        if format.prefix=="oai_dc":
            record=dcRecord(data)
        else: #arXivRaw
            record=arXivRawRecord(data)    
    else:
        data=get_record_data_current(arxiv_id)
        if data is None:
            raise OAINonexistentID("Nothing found for this ID",query_params=query_data)
        if format.prefix=="arXivOld":
            record= arXivOldRecord(data)
        else: #arXiv
            record= arXivRecord(data)

    #TODO format data
    #TODO look into rights statements in the about section
    response=render_template("get_record.xml", 
        response_date=datetime.now(timezone.utc),
        query_params=query_data,
        record=record,
        format=format.prefix
        )
    headers={"Content-Type":"application/xml"}
    return response, 200, headers

