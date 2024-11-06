from typing import Dict

from oaipmh.data.oai_errors import OAIBadArgument
from oaipmh.serializers.output_formats import Response


def get_record(params: Dict[str, str]) -> Response:
    """used to get data on a particular record in a particular metadata format"""

    # get parameters
    expected_params={"identifier", "metadata_prefix", "verb"}
    if set(params.keys()) != expected_params:
        raise OAIBadArgument
    identifier=params["identifier"]
    meta_type=params["metadata_prefix"]

    return "<a>b</a>", 200, {}

def list_records(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_identifiers(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}
