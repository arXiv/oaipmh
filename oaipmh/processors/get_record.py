from typing import Dict
from datetime import datetime, timezone

from flask import render_template

from arxiv.identifier import Identifier
from arxiv.integration.fastly.headers import add_surrogate_key

from oaipmh.processors.db import get_record_data
from oaipmh.data.oai_errors import OAINonexistentID
from oaipmh.data.oai_properties import OAIParams, MetadataFormat
from oaipmh.serializers.create_records import arXivOldRecord, arXivRawRecord, arXivRecord, dcRecord
from oaipmh.serializers.output_formats import Response

def do_get_record(arxiv_id: Identifier, format: MetadataFormat, query_data: Dict[OAIParams, str])-> Response:
    """fetches the required data for a record for a specific format 
    converts data into specific format and renders record template
    """
    data=get_record_data(arxiv_id, format.all_versions)
    if not data:
            raise OAINonexistentID("Nothing found for this ID",query_params=query_data)
    
    match format.prefix:
        case "oai_dc":
            record=dcRecord(data)
        case "arXivRaw":
            record=arXivRawRecord(data)    
        case "arXivOld":
            record= arXivOldRecord(data)
        case "arXiv": 
            record= arXivRecord(data)

    response=render_template("get_record.xml", 
        response_date=datetime.now(timezone.utc),
        query_params=query_data,
        record=record,
        format=format.prefix
        )
    headers={'Surrogate-Control': 'max-age=800000'} 
    headers=add_surrogate_key(headers,[f"paper-id-{arxiv_id.id}", f"paper-id-{arxiv_id.id}-current", "oai-get-record"]) 
    return response, 200, headers

