import json
import uuid

from flask import Blueprint, render_template, url_for, request, Response
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers import action_controller
from app.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_rules', __name__, template_folder='templates')

ACTION_TYPES = {
    "ICL1E",
    "ICL2W",
    "ICL4N",
    "ICHHQE",
    "ICHHQW",
    "ICHHQN"
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
        trigger_date_time = convert_to_iso_timestamp(request.form['trigger_date_time'])
    except ValueError:
        abort(400)

    if request.form.get('classifiers'):
        try:
            classifiers = json.loads(request.form['classifiers'])
        except ValueError:
            abort(Response('Invalid classifiers json', 400))
    else:
        classifiers = None

    action_plan = action_controller.get_action_plan(action_plan_id)

    action_controller.create_action_rule(action_rule_id=request.form.get('action_rule_id') or str(uuid.uuid4()),
                                         trigger_date_time=trigger_date_time,
                                         classifiers=classifiers,
                                         action_plan_url=action_plan['url'],
                                         action_type=request.form['action_type'])
    return redirect(url_for('action_rules.get_action_rules', action_plan_id=action_plan_id))
