from flask import Blueprint

blueprint = Blueprint('general', __name__)


@blueprint.route("/oai", methods=['GET', 'HEAD', 'POST'])
def oai():  # type: ignore
    return "working!", 200, {}