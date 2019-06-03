import uuid

from flask import Blueprint, render_template, request, url_for
from generate_qid_batch import generate_messages_from_config_file
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth

blueprint = Blueprint('generate_qid_batch', __name__, template_folder='templates')


@blueprint.route('/generate-qid-batch', methods=['GET'])
@auth.login_required
def get_generate_qid_batch():
    return render_template('generate_qid_batch.html')


@blueprint.route('/generate-qid-batch', methods=['POST'])
@auth.login_required
def generate_qid_batch():
    if 'config-file' not in request.files:
        abort(400, 'No config file selected')

    try:
        batch_id = uuid.UUID(request.form['batch_id'], version=4) if request.form['batch_id'] else uuid.uuid4()
    except ValueError:
        abort(400, 'Invalid UUID for batch ID')
    batch_config_file_bytes = request.files['config-file'].stream
    batch_config_file = (line.decode() for line in batch_config_file_bytes)

    generate_messages_from_config_file(batch_config_file, batch_id)

    return redirect(url_for('action_plans.get_action_plans'))
