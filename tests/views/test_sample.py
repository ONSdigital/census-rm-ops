from io import BytesIO
from unittest.mock import ANY, patch


def test_get_upload_sample_page(client, requests_mock):
    requests_mock.get('/actionPlans/4c27fcbf-e069-44db-a239-99c9cd70a1d0', json={
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
        }})

    response = client.get('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/sample')

    assert response.status_code == 200
    assert b'Upload a sample for test' in response.data


def test_upload_social_sample_file(client):
    with patch('app.views.load_sample.load_sample') as load_sample_mock:
        response = client.post('/action-plans/4c27fcbf-e069-44db-a239-99c9cd70a1d0/sample',
                               data={'sample': (BytesIO(b'header\nline'), 'sample.csv')})

    load_sample_mock.assert_called_once_with(ANY, collection_exercise_id='4c27fcbf-e069-44db-a239-99c9cd70a1d0',
                                             action_plan_id='4c27fcbf-e069-44db-a239-99c9cd70a1d0')

    assert response.status_code == 302
