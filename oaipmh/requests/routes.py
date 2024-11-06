from typing import Dict
from datetime import datetime, timezone
from flask import Blueprint, request, Response, render_template

from oaipmh.requests.verb_sorter import verb_sorter

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'POST'])
def oai() -> Response:

    #TODO what happens if duplicate params
    params: Dict[str, str] = request.args.to_dict() if request.method == 'GET' else request.form.to_dict()
    result=verb_sorter(params)
    
    response_xml=render_template("base.xml", 
                                 response_date=datetime.now(timezone.utc),
                                 request_info="request info", #TODO
                                 interior_xml="interior data" #TODO
                                 )
    headers={"Content-Type":"application/xml"}

    return response_xml, 200, headers

@blueprint.route('/favicon.ico')
def favicon():
    #TODO
    return '', 204
