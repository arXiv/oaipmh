from datetime import datetime, timezone
from typing import Dict, Any

from flask import render_template

from arxiv.taxonomy.definitions import ARCHIVES_ACTIVE

from oaipmh.data.oai_properties import OAIParams
from oaipmh.serializers.output_formats import Response

def produce_set_list(query_data: Dict[OAIParams, Any]) -> Response:
    """create the set structure of a repository"""
    #TODO display in desired form/ level of depth once decided
    #TODO filter out hidden entries
    response=render_template("setSpec.xml", 
                response_date=datetime.now(timezone.utc),
                query_data=query_data,
                archives=ARCHIVES_ACTIVE)
    return response, 200, {}