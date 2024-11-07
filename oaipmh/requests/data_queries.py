from typing import Dict

from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.serializers.output_formats import Response


def get_record(params: Dict[str, str]) -> Response:
    """used to get data on a particular record in a particular metadata format"""

    # get parameters
    expected_params={"identifier", "metadataPrefix", "verb"}
    if set(params.keys()) != expected_params:
        raise OAIBadArgument
    identifier=params["identifier"]
    meta_type=params["metadataPrefix"]

    #TODO rest of function

    return "<a>b</a>", 200, {}

def list_records(params: Dict[str, str]) -> Response:

    #TODO rest of function

    return "<a>b</a>", 200, {}

def list_identifiers(params: Dict[str, str]) -> Response:
    """retrieves headers of all records matching certain parameters"""
    token=None

    #get parameters
    given_params=set(params.keys())
    if "resumptionToken" in given_params:
        if given_params != {"resumptionToken", "verb"}: #resumption token is exclusive
            raise OAIBadArgument
        token=params["resumptionToken"]
    else:
        if "metadataPrefix" not in given_params:
            raise OAIBadArgument
        allowed_params={"verb","metadataPrefix", "from", "until", "set" }
        if given_params-allowed_params: #no extra keys allowed
            raise OAIBadArgument

        meta_type=params["metadataPrefix"]
        from_str=params.get("from")
        until_str=params.get("until")
        set_str=params.get("set")

    #TODO rest of function
        
    return "<a>b</a>", 200, {}
