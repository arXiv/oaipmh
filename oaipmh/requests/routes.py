from typing import Dict
from flask import Blueprint, request, Response

from oaipmh.requests.verb_sorter import verb_sorter

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'POST'])
def oai() -> Response:

    params: Dict[str, str] = request.args.to_dict() if request.method == 'GET' else request.form.to_dict()
    result=verb_sorter(params)
    #TODO package interior data in page

    return "working", 200, {}