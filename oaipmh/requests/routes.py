from typing import Dict
from datetime import datetime, timezone
from flask import Blueprint, request,  render_template

from oaipmh.requests.verb_sorter import verb_sorter
from oaipmh.serializers.output_formats import Response

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'POST'])
def oai() -> Response:

    #TODO duplicate params dont create errors, technically not to spec
    params: Dict[str, str] = request.args.to_dict() if request.method == 'GET' else request.form.to_dict()
    
    response, code, headers=verb_sorter(params)
    headers["Content-Type"]="application/xml"

    return response, code, headers

@blueprint.route('/favicon.ico')
def favicon():
    #TODO
    return '', 204
