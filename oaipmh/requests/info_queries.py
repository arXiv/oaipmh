from typing import Dict
from datetime import timezone, datetime

from flask import render_template

from arxiv.integration.fastly.headers import add_surrogate_key

from oaipmh.data import oai_config
from oaipmh.data.oai_errors import OAIBadArgument, OAINonexistentID
from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.serializers.output_formats import Response
from oaipmh.processors.create_set_list import display_set_structure
from oaipmh.processors.db import check_paper_existence
from oaipmh.requests.param_processing import process_identifier

def identify(params: Dict[str, str]) -> Response:
    """used to retrieve information about the repository"""
    query_data: Dict[OAIParams, str]={OAIParams.VERB : OAIVerbs.IDENTIFY}
    if set(params.keys()) != {OAIParams.VERB}:
        raise OAIBadArgument(f"No other parameters allowed for {OAIVerbs.IDENTIFY}")
    
    response=render_template("identify.xml",  
        response_date=datetime.now(timezone.utc),
        query_params=query_data,
        config_data=oai_config
        )
    headers={'Surrogate-Control': f'max-age=31536000'} #a year, shouldn't change
    headers=add_surrogate_key(headers,["oai-static"])
    return response, 200, headers

def list_metadata_formats(params: Dict[str, str]) -> Response:
    """used to retrieve the metadata formats available from a repository.
    An optional argument restricts the request to the formats available for a specific item.
    """
    query_data: Dict[OAIParams, str]={OAIParams.VERB : OAIVerbs.LIST_META_FORMATS}

    given_params=set(params.keys())
    expected_params={OAIParams.VERB, OAIParams.ID}
    if OAIParams.ID in given_params: #give formats for one item
        if given_params != expected_params:
            raise OAIBadArgument(f"Only {OAIParams.ID} parameter allowed")
        
        identifier_str=params[OAIParams.ID]
        arxiv_id=process_identifier(identifier_str)
        query_data[OAIParams.ID]=identifier_str
        if not check_paper_existence(arxiv_id):#no formats available for a non existant paper
            raise OAINonexistentID(f"No paper with that ID.", query_data)
     
    else: 
        if given_params != {OAIParams.VERB}:
            raise OAIBadArgument(f"Only allowed parameters are {', '.join(str(param) for param in expected_params)}")
    
    #give formats repository supports
    response=render_template("metaformats.xml", 
        response_date=datetime.now(timezone.utc),
        query_params=query_data,
        formats=oai_config.SUPPORTED_METADATA_FORMATS
        )
    headers={'Surrogate-Control': f'max-age=31536000'} #a year, shouldn't change
    headers=add_surrogate_key(headers,["oai-static"])
    return response, 200, headers

def list_sets(params: Dict[str, str]) -> Response:
    """used to retrieve the set structure of a repository"""
    query_data: Dict[OAIParams, str]={OAIParams.VERB:OAIVerbs.LIST_SETS}
    given_params=set(params.keys())
    if OAIParams.RES_TOKEN in given_params:
        if given_params != {OAIParams.RES_TOKEN, OAIParams.VERB}: #resumption token is exclusive
            raise OAIBadArgument(f"No other paramters allowed with {OAIParams.RES_TOKEN}")
        raise OAIBadArgument(f"Invalid token") #we never give out a resumption token for sets
    else:
        if given_params != {OAIParams.VERB}: 
            raise OAIBadArgument(f"No other parameters allowed")
    return display_set_structure(query_data) 

