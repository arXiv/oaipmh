from flask import Blueprint

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'HEAD'])
def oai():  # type: ignore
    return "working!", 200, {}