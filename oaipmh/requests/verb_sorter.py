from typing import Dict


from oaipmh.requests.info_queries import identify, list_metadata_formats, list_sets
from oaipmh.requests.data_queries import get_record, list_identifiers, list_records
from oaipmh.serializers.output_formats import Response
from oaipmh.data.oai_errors import OAIBadVerb
from oaipmh.data.oai_properties import OAIVerbs

def verb_sorter(params: Dict[str, str]) -> Response:
    """
    sorts OAI queries to the appropriate handler based on their verb statement
    this defines what the client is asking for as per the OAI standard
    further verification of parameters is done with the handlers for individual verbs
    returns the interior xml for the response
    """
    verb = params.get("verb", "")
    match verb:
        case OAIVerbs.GET_RECORD:
            return get_record(params)
        case OAIVerbs.LIST_RECORDS:
            return list_records(params)
        case OAIVerbs.LIST_IDS:
            return list_identifiers(params)
        case OAIVerbs.IDENTIFY:
            return identify(params)
        case OAIVerbs.LIST_META_FORMATS:
            return list_metadata_formats(params)
        case OAIVerbs.LIST_SETS:
            return list_sets(params)
        case _:
            raise OAIBadVerb(f"Invalid verb provided") #dont keep invalid verb
