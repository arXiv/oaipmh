from typing import Dict, Union
import re
from datetime import datetime, timezone, timedelta

from arxiv.taxonomy.definitions import GROUPS, ARCHIVES_ACTIVE, CATEGORIES_ACTIVE
from arxiv.taxonomy.category import Group, Archive, Category

from oaipmh.data.oai_config import SUPPORTED_METADATA_FORMATS, EARLIEST_DATE
from oaipmh.data.oai_errors import OAIBadArgument, OAIBadFormat, OAIBadResumptionToken
from oaipmh.data.oai_properties import OAIParams, OAIVerbs
from oaipmh.processors.get_record import do_get_record
from oaipmh.processors.fetch_list import fetch_list
from oaipmh.processors.resume import ResToken
from oaipmh.serializers.output_formats import Response
from oaipmh.requests.param_processing import process_identifier

DATE_REGEX = r"\d{4}-\d{2}-\d{2}"

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
    query_data[OAIParams.META_PREFIX]=meta_type_str
    return do_get_record(arxiv_id, meta_type, query_data)


def list_data(params: Dict[str, str], just_ids: bool)-> Response:
    """runs both list queries. just_ids true for list identifiers, false for list records"""
    query_data: Dict[OAIParams, str]={OAIParams.VERB:params[OAIParams.VERB]}
    skip_val=0

    #parameter processing
    given_params=set(params.keys())
    if OAIParams.RES_TOKEN in given_params: #get parameters from token
        if given_params != {OAIParams.RES_TOKEN, OAIParams.VERB}: #resumption token is exclusive
            raise OAIBadArgument(f"No other paramters allowed with {OAIParams.RES_TOKEN}")
        token=params[OAIParams.RES_TOKEN]
        token_params, skip_val=ResToken.from_token(token) 
        query_data[OAIParams.RES_TOKEN]=token
        if params[OAIParams.VERB] != token_params[OAIParams.VERB]:
            raise OAIBadResumptionToken("token from different verb", query_data)
        params=token_params #set request parameters from token
        given_params=set(params.keys())
     
    #process request parameters
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
            if not re.fullmatch(DATE_REGEX, from_str):
                raise ValueError
            start_date=datetime.strptime(from_str, "%Y-%m-%d")
            start_date = start_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc)
            query_data[OAIParams.FROM]=from_str
        except Exception:
            raise OAIBadArgument("from date format must be YYYY-MM-DD")
    else:
        start_date=EARLIEST_DATE

    until_str=params.get(OAIParams.UNTIL)
    if until_str:
        try:
            if not re.fullmatch(DATE_REGEX, until_str):
                raise ValueError
            end_date=datetime.strptime(until_str, "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
            query_data[OAIParams.UNTIL]=until_str
        except Exception:
            raise OAIBadArgument("until date format must be YYYY-MM-DD")
    else:
        end_date=datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)

    #sets   
    set_str=params.get(OAIParams.SET)
    if set_str:
        rq_set= _parse_set(set_str)
        query_data[OAIParams.SET]=set_str
        if not rq_set.is_active or 'test' in rq_set.id:
            raise OAIBadArgument("Invalid set request")
    else:
        rq_set=None

    #dates are valid
    if start_date>end_date:
        raise OAIBadArgument("until date must be greater than or equal to from date")
    if start_date < EARLIEST_DATE:
        raise OAIBadArgument("start date too early")
    if end_date> datetime.now(timezone.utc) + timedelta(days=1):
        raise OAIBadArgument("until date too late")

    return fetch_list(just_ids, start_date, end_date, meta_type, rq_set, skip_val , query_data)

def _parse_set(set_str:str)-> Union[Group, Archive, Category]:
    """turns OAI style string into taxonomy item
        validates item
    """
    set_parts=set_str.split(":")
    match len(set_parts):
        case 1: #asking for a group
            rq_set = GROUPS.get(f'grp_{set_str}')
            if not rq_set:
                raise OAIBadArgument("Set does not exist")
        case 2: #archive (including archive as category)
            grp_str, archive_str = set_parts
            rq_set = ARCHIVES_ACTIVE.get(archive_str)
            if not rq_set or f'grp_{grp_str}' != rq_set.in_group:
                raise OAIBadArgument("Set does not exist")
        case 3: #full category
            grp_str, archive_str, category_suffix = set_parts
            cat_str = f"{archive_str}.{category_suffix}"
            if cat_str not in CATEGORIES_ACTIVE:
                raise OAIBadArgument("Set does not exist")
            rq_set= CATEGORIES_ACTIVE[cat_str]
            archive= rq_set.get_archive()
            if archive_str!= archive.id or f'grp_{grp_str}' != archive.in_group:
                raise OAIBadArgument("Set does not exist")
        case _:
            raise OAIBadArgument("Set has too many levels")
        
    return rq_set



