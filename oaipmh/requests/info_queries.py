from typing import Dict

from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.serializers.output_formats import Response

def identify(params: Dict[str, str]) -> Response:
    """used to retrieve information about the repository"""
    if set(params.keys()) != {"verb"}:
        raise OAIBadArgument

    return "<a>b</a>", 200, {}

def list_metadata_formats(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_sets(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}
