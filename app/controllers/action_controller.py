import requests
from flask import current_app as app


def create_action_type(action_type_id, name, description, handler):
    url = f'{app.config["ACTION_SERVICE"]}/actionTypes'
    body = {'id': action_type_id, 'name': name, 'description': description, 'handler': handler}

    response = requests.post(url, auth=app.config["BASIC_AUTH"], json=body)
    response.raise_for_status()

    return response.json()


def create_action_rule(action_rule_id, trigger_date_time, classifiers, action_plan_url, action_type_url,
                       has_triggered=False):
    url = f'{app.config["ACTION_SERVICE"]}/actionRules'
    body = {'id': action_rule_id, 'triggerDateTime': trigger_date_time, 'classifiers': classifiers,
            'actionPlan': action_plan_url, 'actionType': action_type_url, 'hasTriggered': has_triggered}

    response = requests.post(url, auth=app.config["BASIC_AUTH"], json=body)
    response.raise_for_status()

    return response.json()


def get_action_plans():
    response = requests.get(
        f"{app.config['ACTION_SERVICE']}/actionPlans",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    action_plans = [{'id': action_plan['_links']['self']['href'].split('/')[-1],
                     'name': action_plan['name'],
                     'description': action_plan['description'],
                     'url': action_plan['_links']['self']['href']}
                    for action_plan in response.json()['_embedded']['actionPlans']]
    return action_plans


def get_action_plan(action_plan_id):
    response = requests.get(
        f"{app.config['ACTION_SERVICE']}/actionPlans/{action_plan_id}",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    action_plan = response.json()
    return {'id': action_plan['_links']['self']['href'].split('/')[-1],
            'name': action_plan['name'],
            'description': action_plan['description'],
            'url': action_plan['_links']['self']['href']}


def create_action_plan(action_plan):
    response = requests.post(f"{app.config['ACTION_SERVICE']}/actionPlans", auth=app.config['BASIC_AUTH'],
                             json=action_plan)
    response.raise_for_status()
    return response.json()


def get_action_rules(action_plan_id):
    response = requests.get(
        f"{app.config['ACTION_SERVICE']}/actionPlans/{action_plan_id}/actionRules",
        auth=app.config['BASIC_AUTH'])
    response.raise_for_status()
    return response.json()
