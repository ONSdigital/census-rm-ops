import uuid

import requests
from flask import Blueprint, request, redirect, url_for, abort, render_template
from flask import current_app as app

from app.auth import auth
from app.controllers import action_controller

blueprint = Blueprint('action_plans', __name__, template_folder='templates')


@blueprint.route('/', methods=['GET'])
@auth.login_required
def index():
    return redirect(url_for('action_plans.get_action_plans'))


@blueprint.route('/action-plans', methods=['GET'])
@auth.login_required
def get_action_plans():
    return render_template('action_plans.html', action_plans=action_controller.get_action_plans())


@blueprint.route('/action-plans/<action_plan_id>', methods=['GET'])
@auth.login_required
def get_action_plan(action_plan_id):
    return render_template('action_plan.html', action_plan=action_controller.get_action_plan(action_plan_id))


@blueprint.route('/action-plans', methods=['POST'])
@auth.login_required
def create_action_plan():
    action_plan = {
        'id':   request.form['action_plan_id'] or str(uuid.uuid4()),
        'name': request.form['name'],
        'description': request.form['description'],
    }
    action_controller.create_action_plan(action_plan)
    return redirect(url_for('action_plans.get_action_plans'))
