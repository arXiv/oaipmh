from typing import Dict
from oaipmh.serializers.output_formats import Response


def get_record(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_records(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}

def list_identifiers(params: Dict[str, str]) -> Response:
    return "<a>b</a>", 200, {}
