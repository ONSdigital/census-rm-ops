def test_get_action_plan_page(client, requests_mock):
    requests_mock.get('/actionPlans', json={"_embedded": {"actionPlans": []}})

    response = client.get('/action-plans')

    assert response.status_code == 200


def test_create_action_plan(client, requests_mock):
    requests_mock.get('/actionPlans', json={"_embedded": {"actionPlans": []}})
    requests_mock.post('/actionPlans', json={})

    client.get('/action-plans')
    response = client.post('/action-plans', data={'name': 'Test', 'description': 'Test description'})

    assert response.status_code == 302


# def test_get_action_rule_page(client, requests_mock):
#     requests_mock.get('/collectionexercises/123', json={})
#     requests_mock.get('/actionplans', json={})
#     requests_mock.get('/surveys/CEN', json={})
#
#     response = client.get('/survey/CEN/collection/123/actions')
#
#     assert response.status_code == 200
#
#
# def test_get_action_rule_page_lists_action_plans_and_rules(client, requests_mock):
#     requests_mock.get('/surveys/CEN', json={})
#     requests_mock.get('/collectionexercises/123', json={})
#     requests_mock.get('/actionplans', json=[{'id': 123, 'name': 'Action plan 1',
#                                              'selectors': {'collectionExerciseId': '123'}}])
#     requests_mock.get('/actionrules/actionplan/123', json=[{'name': 'Action rule 1', 'triggerDateTime': '1'}])
#
#     response = client.get('/survey/CEN/collection/123/actions')
#
#     assert b'Action plan 1' in response.data
#     assert b'Action rule 1' in response.data
#
#
# def test_create_action_rule(client, requests_mock):
#     requests_mock.get('/actionplans', json={})
#     requests_mock.post('/actionrules')
#     response = client.post('/survey/CEN/collection/123/actions', data={
#         'action_plan_id': '123',
#         'action_rule_type': 'ICL1E',
#         'name': 'Initial Contact Letter (England)',
#         'description': 'Initial Contact Letter (England)',
#         'timestamp': '2010-01-02T01:01',
#         'priority': '3',
#     })
#
#     assert response.status_code == 302
#
#
# def test_create_action_rule_fails(client, requests_mock):
#     requests_mock.get('/actionplans', json={})
#     requests_mock.post('/actionrules', status_code=500)
#     response = client.post('/survey/CEN/collection/123/actions', data={
#         'action_plan_id': '123',
#         'action_rule_type': 'ICL1E',
#         'name': 'Initial Contact Letter (England)',
#         'description': 'Initial Contact Letter (England)',
#         'timestamp': '2010-01-02T01:01',
#         'priority': '3',
#     })
#
#     assert response.status_code == 500
#
#
# def test_create_action_rule_missing_data(client, requests_mock):
#     requests_mock.get('/actionplans', json={})
#
#     response = client.post('/survey/CEN/collection/123/actions')
#
#     assert response.status_code == 400
