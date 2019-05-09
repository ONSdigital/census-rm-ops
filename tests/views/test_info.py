def test_get_healthcheck(client):
    response = client.get('/info')
    assert response.status_code == 200
