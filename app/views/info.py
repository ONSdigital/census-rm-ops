from flask import Blueprint, Response

blueprint = Blueprint('info', __name__, template_folder='templates')


@blueprint.route('/info', methods=["GET"])
def get_health():
    return Response(status=200)
