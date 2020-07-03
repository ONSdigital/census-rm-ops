import uuid

from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers import action_controller
from app.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_rules', __name__, template_folder='templates')

ACTION_TYPES = {
    'Field': ["FIELD"],
    'Initial contact letters HH': [
        "ICL1E",
        "ICL2W",
        "ICL4N",
    ],

    'Initial contact letter CE1': [
        "CE1_IC01",
        "CE1_IC02",
    ],
    'Initial contact letter CE Estab Individual': [
        "CE_IC03",
        "CE_IC04",
    ],
    'Initial contact letter CE Unit Individual': [
        "CE_IC03_1",
        "CE_IC04_1",
    ],
    'Initial contact letter CE Individual (NI)': [
        "CE_IC05",
        "CE_IC06",
    ],
    'Initial contact letter SPG': [
        "SPG_IC11",
        "SPG_IC12",
    ],
    "Initial contact q'naires HH": [
        "ICHHQE",
        "ICHHQW",
        "ICHHQN",
    ],
    "Initial contact q'naires CE Individual": [
        "CE_IC08",
        "CE_IC09",
        "CE_IC10",
    ],
    "Initial contact q'naires SPG": [
        "SPG_IC13",
        "SPG_IC14",
    ],

    'Reminder letters': [
        "P_RL_1RL1_1",
        "P_RL_1RL2B_1",
        "P_RL_1RL4",
        "P_RL_1RL1_2",
        "P_RL_1RL2B_2",
        "P_RL_2RL1_3a",
        "P_RL_2RL2B_3a",
    ],
    'Reminder letters, response driven': [

        "P_RD_2RL1_1",
        "P_RD_2RL2B_1",
        "P_RD_2RL1_2",
        "P_RD_2RL2B_2",
        "P_RD_2RL1_3",
        "P_RD_2RL2B_3",
    ],
    'Reminder letters, survey launched': [
        "P_RL_1RL1A",
        "P_RL_1RL2BA",
        "P_RL_2RL1A",
        "P_RL_2RL2BA",

    ],

    "Reminder q'naires": [
        "P_QU_H1",
        "P_QU_H2",
        "P_QU_H4",
    ],

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
        abort(400, 'Invalid trigger date time')

    if not request.form.get('where_clause') or not request.form.get('where_clause').strip():
        abort(400, 'Empty where clause')

    if request.form.get('where_clause').strip().endswith('AND'):
        abort(400, 'Invalid where clause')

    where_clause = request.form['where_clause']

    action_plan = action_controller.get_action_plan(action_plan_id)

    action_controller.create_action_rule(action_rule_id=request.form.get('action_rule_id') or str(uuid.uuid4()),
                                         trigger_date_time=trigger_date_time,
                                         where_clause=where_clause,
                                         action_plan_url=action_plan['url'],
                                         action_type=request.form['action_type'])
    return redirect(url_for('action_rules.get_action_rules', action_plan_id=action_plan_id))
