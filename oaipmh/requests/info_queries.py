from typing import Dict

from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.data.oai_properties import OAIParams
from oaipmh.serializers.output_formats import Response

def identify(params: Dict[str, str]) -> Response:
    """used to retrieve information about the repository"""
    if set(params.keys()) != {OAIParams.VERB}:
        raise OAIBadArgument

    return "<a>b</a>", 200, {}

def list_metadata_formats(params: Dict[str, str]) -> Response:
    """used to retrieve the metadata formats available from a repository.
    An optional argument restricts the request to the formats available for a specific item.
    """

    given_params=set(params.keys())
    if OAIParams.ID in given_params: #give formats for one item
        if given_params != {OAIParams.VERB, OAIParams.ID}:
            raise OAIBadArgument
        #TODO get formats for an item
        return "<a>b</a>", 200, {}

    else: #give formats repository supports
        if given_params != {OAIParams.VERB}:
            raise OAIBadArgument
        #TODO get formats for repository
        return "<a>b</a>", 200, {}

def list_sets(params: Dict[str, str]) -> Response:
    """used to retrieve the set structure of a repository"""

    token=None
    #get parameters
    given_params=set(params.keys())
    if OAIParams.RES_TOKEN in given_params:
        if given_params != {OAIParams.RES_TOKEN, OAIParams.VERB}: #resumption token is exclusive
            raise OAIBadArgument
        token=params[OAIParams.RES_TOKEN]
        #TODO will we ever hit this, or will we always return our set structure in full?
    else:
        if given_params != {OAIParams.VERB}: 
            raise OAIBadArgument

    #TODO rest of function

    return "<a>b</a>", 200, {}
