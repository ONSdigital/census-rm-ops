from tests.views import ACTION_PLAN


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
