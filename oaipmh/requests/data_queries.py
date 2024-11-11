from typing import Dict
import re
from datetime import datetime, timezone

from oaipmh.data.oai_config import SUPPORTED_METADATA_FORMATS, EARLIEST_DATE
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

    #parameter processing
    given_params=set(params.keys())
    if OAIParams.RES_TOKEN in given_params: #using resumption token
        if given_params != {OAIParams.RES_TOKEN, OAIParams.VERB}: #resumption token is exclusive
            raise OAIBadArgument(f"No other paramters allowed with {OAIParams.RES_TOKEN}")
        token=params[OAIParams.RES_TOKEN]
        #TODO token processing and validation

    else: #using request parameters
        #correct parameters present
        if OAIParams.META_PREFIX not in given_params:
            raise OAIBadArgument(f"{OAIParams.META_PREFIX} required.")
        allowed_params={OAIParams.VERB,OAIParams.META_PREFIX, OAIParams.FROM, OAIParams.UNTIL, OAIParams.SET }
        if given_params-allowed_params: #no extra keys allowed
            raise OAIBadArgument(f"Unallowed parameter. Allowed parameters: {', '.join(str(param) for param in allowed_params)}")

        #metadata
        meta_type_str=params[OAIParams.META_PREFIX]
        if meta_type_str not in SUPPORTED_METADATA_FORMATS:
            raise OAIBadFormat(reason="Did not recognize requested format", query_params=query_data)
        meta_type=SUPPORTED_METADATA_FORMATS[meta_type_str]
        query_data[OAIParams.META_PREFIX]=meta_type_str

        #dates
        from_str=params.get(OAIParams.FROM)
        if from_str:
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", from_str):
                    raise ValueError
                start_date=datetime.strptime(from_str, "%Y-%m-%d")
                start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
                query_data[OAIParams.FROM]=from_str
            except Exception:
                raise OAIBadArgument("from date format must be YYYY-MM-DD")
        else:
            start_date=EARLIEST_DATE

        until_str=params.get(OAIParams.UNTIL)
        if until_str:
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", until_str):
                    raise ValueError
                end_date=datetime.strptime(until_str, "%Y-%m-%d")
                end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
                query_data[OAIParams.UNTIL]=until_str
            except Exception:
                raise OAIBadArgument("until date format must be YYYY-MM-DD")
        else:
            end_date=datetime.now(timezone.utc)

        #sets
        set_str=params.get(OAIParams.SET)
        #TODO paramter processing

    #TODO check that combined parameters are valid (dates are okay)

    #TODO rest of function

    return "<a>b</a>", 200, {}