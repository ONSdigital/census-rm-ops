import uuid

from flask import Blueprint, render_template, url_for, request
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.auth import auth
from app.controllers import action_controller
from app.timestamp import convert_to_iso_timestamp

blueprint = Blueprint('action_rules', __name__, template_folder='templates')

ACTION_TYPES = {
    "FIELD",

    "ICL1E",
    "ICL2W",
    "ICL4N",

    "ICHHQE",
    "ICHHQW",
    "ICHHQN",

    "P_RL_1RL1_1",
    "P_RL_1RL2B_1",
    "P_RL_1RL4",
    "P_RL_1RL1_2",
    "P_RL_1RL2B_2",
    "P_RL_2RL1_3a",
    "P_RL_2RL2B_3a",

    "P_RL_1RL1A",
    "P_RL_1RL2BA",
    "P_RL_2RL1A",
    "P_RL_2RL2BA",

    "P_RD_2RL1_1",
    "P_RD_2RL2B_1",
    "P_RD_2RL1_2",
    "P_RD_2RL2B_2",
    "P_RD_2RL1_3",
    "P_RD_2RL2B_3",

    "P_QU_H1",
    "P_QU_H2",
    "P_QU_H4",

    "CE1_IC01",
    "CE1_IC02",

    "CE_IC03",
    "CE_IC04",
    "CE_IC05",
    "CE_IC06",
    "CE_IC08",
    "CE_IC09",
    "CE_IC10",

    "CE_IC03_1",
    "CE_IC04_1",

    "SPG_IC11",
    "SPG_IC12",
    "SPG_IC13",
    "SPG_IC14",
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

    if request.form.get('where_clause'):
        where_clause = request.form['where_clause']
    else:
        where_clause = None

    action_plan = action_controller.get_action_plan(action_plan_id)

    action_controller.create_action_rule(action_rule_id=request.form.get('action_rule_id') or str(uuid.uuid4()),
                                         trigger_date_time=trigger_date_time,
                                         where_clause=where_clause,
                                         action_plan_url=action_plan['url'],
                                         action_type=request.form['action_type'])
    return redirect(url_for('action_rules.get_action_rules', action_plan_id=action_plan_id))
