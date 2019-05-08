def test_get_action_plans_page(client, requests_mock):
    requests_mock.get('/actionPlans', json={"_embedded": {"actionPlans": []}})

    response = client.get('/action-plans')

    assert response.status_code == 200
    assert b'Action Plans' in response.data
    assert b'Create an action plan' in response.data


def test_get_root_redirects_to_action_plans_page(client, requests_mock):
    requests_mock.get('/actionPlans', json={"_embedded": {"actionPlans": []}})

    response = client.get('/', follow_redirects=True)

    assert response.status_code == 200
    assert b'Action Plans' in response.data
    assert b'Create an action plan' in response.data


def test_create_action_plan(client, requests_mock):
    requests_mock.get('/actionPlans', json={"_embedded": {"actionPlans": []}})
    requests_mock.post('/actionPlans', json={})

    client.get('/action-plans')
    response = client.post('/action-plans', data={'name': 'Test', 'description': 'Test description'},
                           follow_redirects=True)

    assert response.status_code == 200


def test_get_action_plan_page(client, requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json=ACTION_PLAN)

    response = client.get('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0')

    assert response.status_code == 200
    assert b'test name' in response.data
    assert b'test description' in response.data


def test_get_action_rules(client, requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json=ACTION_PLAN)
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules', json=ACTION_RULES)

    response = client.get('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules')

    assert response.status_code == 200
    assert b'Current action rules' in response.data
    assert b'Create action rule' in response.data
    assert b'ICL1E' in response.data


def test_create_action_rule(client, requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json=ACTION_PLAN)
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules', json=ACTION_RULES)
    requests_mock.post('/actionRules', json={})
    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
    }, follow_redirects=True)

    assert response.status_code == 200


def test_invalid_classifiers_json_responds_400(client, requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json=ACTION_PLAN)
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules', json=ACTION_RULES)
    requests_mock.post('/actionRules', json={})
    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
        'classifiers': 'not valid json'
    }, follow_redirects=True)

    assert response.status_code == 400
    assert b'Invalid classifiers json' in response.data


ACTION_PLAN = {
    "name": "test name",
    "description": "test description",
    "_links": {
        "self": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0"
        },
        "actionPlan": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0"
        },
        "actionRules": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules"
        }
    }}

ACTION_RULES = {
    "_embedded": {
        "actionRules": [{
            "actionType": "ICL1E",
            "triggerDateTime": "2019-05-08T08:00:00Z",
            "hasTriggered": False,
            "classifiers": None,
            "_links": {
                "self": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9"
                },
                "actionRule": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9"
                },
                "actionPlan": {
                    "href": "http://localhost:8301/actionRules/156ba07d-37eb-4836-a1fb-3ab1580c1cf9/actionPlan"
                }
            }
        }]
    },
    "_links": {
        "self": {
            "href": "http://localhost:8301/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules"
        }
    }
}
