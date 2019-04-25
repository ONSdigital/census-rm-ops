import uuid

from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers import action_controller
from app.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_plan', __name__, template_folder='templates')

# Get this from an endpoint (That doesn't exist yet)
ACTION_TYPES = {
    "ICL1E"
}


@auth.login_required
@blueprint.route('/action-plans/<action_plan_id>/action-rules', methods=['GET'])
def get_action_rules(action_plan_id):
    action_plan = action_controller.get_action_plan(action_plan_id)
    return render_template('action_rules.html', action_types=ACTION_TYPES,
                           action_rules=action_controller.get_action_rules(action_plan_id),
                           action_plan=action_plan)


@blueprint.route('/action-plans/<action_plan_id>/action-rules', methods=["POST"])
def create_action_rule(action_plan_id):
    try:
        timestamp = convert_to_iso_timestamp(request.form['timestamp'])
    except ValueError:
        abort(400)
    action_plan = action_controller.get_action_plan(action_plan_id)

    # TODO replace hardcoded action type link
    action_controller.create_action_rule(action_rule_id=str(uuid.uuid4()), trigger_date_time=timestamp,
                                         classifiers=request.form['classifiers'], action_plan_url=action_plan['link'],
                                         action_type_url=
                                         'http://localhost:8151/actionTypes/5dac94a9-3b5f-4fb7-b5e8-ccc108e14059')
    return redirect(url_for('action_rules.get_action_rules', action_plan_id=action_plan_id))
