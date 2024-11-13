from typing import Dict
from flask import Blueprint, request

from oaipmh.requests.info_queries import identify, list_metadata_formats, list_sets
from oaipmh.requests.data_queries import get_record, list_identifiers, list_records
from oaipmh.serializers.output_formats import Response
from oaipmh.data.oai_errors import OAIBadVerb
from oaipmh.data.oai_properties import OAIVerbs
from oaipmh.serializers.output_formats import Response

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'POST'])
def oai() -> Response:
    """
    sorts OAI queries to the appropriate handler based on their verb statement
    this defines what the client is asking for as per the OAI standard
    further verification of parameters is done with the handlers for individual verbs
    """
    #TODO duplicate params dont create errors, technically not to spec
    params: Dict[str, str] = request.args.to_dict() if request.method == 'GET' else request.form.to_dict()
    verb = params.get("verb", "")
    match verb:
        case OAIVerbs.GET_RECORD:
            response, code, headers= get_record(params)
        case OAIVerbs.LIST_RECORDS:
            response, code, headers= list_records(params)
        case OAIVerbs.LIST_IDS:
            response, code, headers= list_identifiers(params)
        case OAIVerbs.IDENTIFY:
            response, code, headers= identify(params)
        case OAIVerbs.LIST_META_FORMATS:
            response, code, headers= list_metadata_formats(params)
        case OAIVerbs.LIST_SETS:
            response, code, headers= list_sets(params)
        case _:
            raise OAIBadVerb(f"Invalid verb provided") #dont keep invalid verb
        
    headers["Content-Type"]="application/xml"

    return response, code, headers

@blueprint.route('/favicon.ico')
def favicon():
    #TODO
    return '', 204
