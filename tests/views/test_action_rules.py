from tests.views import ACTION_PLAN, ACTION_RULES


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
