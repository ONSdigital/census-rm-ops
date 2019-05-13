from io import BytesIO
from unittest.mock import patch


def test_get_upload_sample_page(client):
    response = client.get('/generate-qid-batch')

    assert response.status_code == 200
    assert b'Upload a QID batch config file' in response.data


def test_upload_qid_batch_config_file(client):
    with patch('app.views.generate_qid_batch.generate_messages_from_config_file') as generate_messages_from_config_file_patch:
        response = client.post('/generate-qid-batch',
                               data={'config-file': (BytesIO(b'header\nline'), 'config-file.csv')})

    generate_messages_from_config_file_patch.assert_called_once()

    assert response.status_code == 302
