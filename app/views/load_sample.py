from flask import Blueprint, render_template, url_for, request
from flask import current_app as app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from load_sample import load_sample

from app.auth import auth
from app.controllers import action_controller

blueprint = Blueprint('load_sample', __name__, template_folder='templates')


@blueprint.route('/action-plans/<action_plan_id>/sample', methods=['GET'])
@auth.login_required
def get_sample(action_plan_id):
    return render_template('load_sample.html', action_plan=action_controller.get_action_plan(action_plan_id))


@blueprint.route('/action-plans/<action_plan_id>/sample', methods=['POST'])
@auth.login_required
def upload_sample(action_plan_id):
    if 'sample' not in request.files:
        abort(400, 'No sample file selected')

    sample_file_in_bytes = request.files['sample'].stream
    sample_file = (line.decode() for line in sample_file_in_bytes)

    # For convenience use the action plan ID as the collection exercise ID
    load_sample(sample_file, collection_exercise_id=action_plan_id,
                action_plan_id=action_plan_id, host=app.config["RABBITMQ_HOST"], port=app.config["RABBITMQ_PORT"],
                vhost=app.config["RABBITMQ_VHOST"], exchange=app.config["RABBITMQ_EXCHANGE"],
                user=app.config["RABBITMQ_USER"], password=app.config["RABBITMQ_PASSWORD"],
                queue_name=app.config["RABBITMQ_QUEUE"])

    return redirect(url_for('action_plans.get_action_plan', action_plan_id=action_plan_id))
