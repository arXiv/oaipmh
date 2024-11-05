from typing import Dict

from oaipmh.requests.info_queries import identify, list_metadata_formats, list_sets
from oaipmh.requests.data_queries import get_record, list_identifiers, list_records
from oaipmh.serializers.output_formats import InteriorData

def verb_sorter(params: Dict[str, str]) -> InteriorData:
    """
    sorts OAI queries to the appropriate handler based on their verb statement
    this defines what the client is asking for as per the OAI standard
    further verification of parameters is done with the handlers for individual verbs
    returns the interior xml for the response
    """
    verb = params.get("verb", "")
    match verb:
        case "GetRecord":
            return get_record(params)
        case "ListRecords":
            return list_records(params)
        case "ListIdentifiers":
            return list_identifiers(params)
        case "Identify":
            return identify(params)
        case "ListMetadataFormats":
            return list_metadata_formats(params)
        case "ListSets":
            return list_sets(params)
        case _:
            #TODO bad/no verb case error
            return InteriorData()
