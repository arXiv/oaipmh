from typing import Dict
from datetime import datetime

from oaipmh.data.oai_config import SUPPORTED_METADATA_FORMATS
from oaipmh.data.oai_errors import OAIBadArgument, OAIBadFormat
from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.serializers.output_formats import Response
from oaipmh.requests.param_processing import process_identifier


def get_record(params: Dict[str, str]) -> Response:
    """used to get data on a particular record in a particular metadata format"""
    query_data: Dict[OAIParams, str]={OAIParams.VERB:OAIVerbs.GET_RECORD}

    # get parameters
    expected_params={OAIParams.ID, OAIParams.META_PREFIX, OAIParams.VERB}
    if set(params.keys()) != expected_params:
        raise OAIBadArgument(f"Parameters provided did not match expected. Expected: {', '.join(str(param) for param in expected_params)}")
    
    identifier_str=params[OAIParams.ID]
    arxiv_id=process_identifier(identifier_str)
    query_data[OAIParams.ID]=identifier_str

    meta_type_str=params[OAIParams.META_PREFIX]
    if meta_type_str not in SUPPORTED_METADATA_FORMATS:
        raise OAIBadFormat(reason="Did not recognize requested format", query_params=query_data)
    meta_type=SUPPORTED_METADATA_FORMATS[meta_type_str]

    #TODO rest of function

    return "<a>b</a>", 200, {}

def list_records(params: Dict[str, str]) -> Response:
    """used to harvest records from a repository with support for selective harvesting"""
    return _list_data(params, False)

def list_identifiers(params: Dict[str, str]) -> Response:
    """retrieves headers of all records matching certain parameters"""
    return _list_data(params, True)


def _list_data(params: Dict[str, str], just_ids: bool)-> Response:
    """runs both list queries. just_ids true for list identifiers, false for list records"""
    query_data: Dict[OAIParams, str]={OAIParams.VERB:OAIVerbs.LIST_IDS}

    #get parameters
    given_params=set(params.keys())
    if OAIParams.RES_TOKEN in given_params:
        if given_params != {OAIParams.RES_TOKEN, OAIParams.VERB}: #resumption token is exclusive
            raise OAIBadArgument(f"No other paramters allowed with {OAIParams.RES_TOKEN}")
        token=params[OAIParams.RES_TOKEN]
        #TODO token processing and validation
    else:
        if OAIParams.META_PREFIX not in given_params:
            raise OAIBadArgument(f"{OAIParams.META_PREFIX} required.")
        allowed_params={OAIParams.VERB,OAIParams.META_PREFIX, OAIParams.FROM, OAIParams.UNTIL, OAIParams.SET }
        if given_params-allowed_params: #no extra keys allowed
            raise OAIBadArgument(f"Unallowed parameter. Allowed parameters: {', '.join(str(param) for param in allowed_params)}")

        meta_type_str=params[OAIParams.META_PREFIX]
        if meta_type_str not in SUPPORTED_METADATA_FORMATS:
            raise OAIBadFormat(reason="Did not recognize requested format", query_params=query_data)
        meta_type=SUPPORTED_METADATA_FORMATS[meta_type_str]
        
        from_str=params.get(OAIParams.FROM)
        until_str=params.get(OAIParams.UNTIL)
        set_str=params.get(OAIParams.SET)
        #TODO paramter processing

    return "<a>b</a>", 200, {}