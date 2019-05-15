from flask import Blueprint, render_template, request, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.generate_qid_batch import generate_messages_from_config_file

blueprint = Blueprint('generate_qid_batch', __name__, template_folder='templates')


@blueprint.route('/generate-qid-batch', methods=['GET'])
@auth.login_required
def get_generate_qid_batch():
    return render_template('generate_qid_batch.html')


@blueprint.route('/generate-qid-batch', methods=['POST'])
@auth.login_required
def generate_qid_batch():
    if 'config-file' not in request.files:
        abort(400)

    batch_config_file_bytes = request.files['config-file'].stream
    batch_config_file = (line.decode() for line in batch_config_file_bytes)

    generate_messages_from_config_file(batch_config_file)

    return redirect(url_for('action_plans.get_action_plans'))
