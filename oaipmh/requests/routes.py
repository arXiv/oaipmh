from typing import Dict
from flask import Blueprint, request, send_file

from arxiv.integration.fastly.headers import add_surrogate_key

from oaipmh.requests.info_queries import identify, list_metadata_formats, list_sets
from oaipmh.requests.data_queries import get_record, list_data
from oaipmh.serializers.output_formats import Response
from oaipmh.data.oai_errors import OAIBadVerb, OAIBadArgument
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
    param_source=request.args if request.method == 'GET' else request.form
    for _, values in param_source.lists():
        if len(values) > 1:
            raise OAIBadArgument("Duplicate parameters not allowed")
    params: Dict[str, str] = param_source.to_dict()

    verb = params.get("verb", "")
    match verb:
        case OAIVerbs.GET_RECORD:
            response, code, headers= get_record(params)
        case OAIVerbs.LIST_RECORDS:
            response, code, headers= list_data(params, False)
        case OAIVerbs.LIST_IDS:
            response, code, headers= list_data(params, True)
        case OAIVerbs.IDENTIFY:
            response, code, headers= identify(params)
        case OAIVerbs.LIST_META_FORMATS:
            response, code, headers= list_metadata_formats(params)
        case OAIVerbs.LIST_SETS:
            response, code, headers= list_sets(params)
        case _:
            raise OAIBadVerb(f"Invalid verb provided") #dont keep invalid verb
        
    headers["Content-Type"]="application/xml"
    headers=add_surrogate_key(headers,["oai"])

    return response, code, headers

@blueprint.route("/OAI/arXivRaw.xsd", methods=['GET', 'POST'])
def schema_arXivRaw() -> Response:
    file_path = "templates/schema/arXivRaw.xsd" 
    return send_file(file_path, mimetype="application/xml")


@blueprint.route("/OAI/arXiv.xsd", methods=['GET', 'POST'])
def schema_arXiv() -> Response:
    file_path = "templates/schema/arXiv.xsd" 
    return send_file(file_path, mimetype="application/xml")

@blueprint.route("/OAI/arXivOld.xsd", methods=['GET', 'POST'])
def schema_arXivOld() -> Response:
    file_path = "templates/schema/arXivOld.xsd" 
    return send_file(file_path, mimetype="application/xml")

@blueprint.route('/favicon.ico')
def favicon():
    #TODO
    return '', 204
