from typing import Dict
from oaipmh.serializers.output_formats import Response

def identify(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_metadata_formats(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_sets(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}
