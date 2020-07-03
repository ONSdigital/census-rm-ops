from tests.views import ACTION_PLAN, ACTION_RULES


def test_get_action_rules(client, requests_mock):
    mock_gets_from_action_scheduler(requests_mock)

    response = client.get('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules')

    assert response.status_code == 200
    assert b'Current action rules' in response.data
    assert b'Create action rule' in response.data
    assert b'ICL1E' in response.data


def test_create_action_rule(client, requests_mock):
    mock_gets_from_action_scheduler(requests_mock)
    mock_post_to_action_scheduler(requests_mock)

    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
        'where_clause': "case_type != 'HI'"
    }, follow_redirects=True)

    assert response.status_code == 200


def test_invalid_classifiers_responds_400(client, requests_mock):
    mock_gets_from_action_scheduler(requests_mock)
    mock_post_to_action_scheduler(requests_mock)

    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
        'where_clause': "case_type != 'HI' AND "
    }, follow_redirects=True)

    assert response.status_code == 400
    assert b'Invalid where clause' in response.data


def test_missing_classifiers_responds_400(client, requests_mock):
    mock_gets_from_action_scheduler(requests_mock)
    mock_post_to_action_scheduler(requests_mock)

    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
    }, follow_redirects=True)

    assert response.status_code == 400
    assert b'Empty where clause' in response.data


def test_empty_classifiers_responds_400(client, requests_mock):
    mock_gets_from_action_scheduler(requests_mock)
    mock_post_to_action_scheduler(requests_mock)

    response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/action-rules', data={
        'trigger_date_time': '2019-05-08T09:00',
        'action_type': 'ICL1E',
        'where_clause': ' '
    }, follow_redirects=True)

    assert response.status_code == 400
    assert b'Empty where clause' in response.data


def mock_gets_from_action_scheduler(requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json=ACTION_PLAN)
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/actionRules', json=ACTION_RULES)


def mock_post_to_action_scheduler(requests_mock):
    requests_mock.post('/actionRules', json={})
