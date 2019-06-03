import uuid
from io import BytesIO
from unittest.mock import patch


def test_get_upload_generate_qid_batch_page(client):
    response = client.get('/generate-qid-batch')

    assert response.status_code == 200
    assert b'Upload a QID batch config file' in response.data


def test_upload_qid_batch_config_file_empty_batch_id(client):
    # Given
    post_data = {'config-file': (BytesIO(b'config\nfile'), 'config-file.csv'), 'batch_id': ''}

    # When
    generate_messages_from_config_file_patch, response = post_to_generate_qid_batch(client, post_data)

    # Then
    generate_messages_from_config_file_patch.assert_called_once()
    assert response.status_code == 302
    call_batch_id = generate_messages_from_config_file_patch.call_args[0][1]
    assert isinstance(call_batch_id, uuid.UUID)


def test_upload_qid_batch_config_file_with_batch_id(client):
    # Given
    batch_id = uuid.uuid4()
    post_data = {'config-file': (BytesIO(b'config\nfile'), 'config-file.csv'), 'batch_id': batch_id}

    # When
    generate_messages_from_config_file_patch, response = post_to_generate_qid_batch(client, post_data)

    # Then
    generate_messages_from_config_file_patch.assert_called_once()
    assert response.status_code == 302
    call_batch_id = generate_messages_from_config_file_patch.call_args[0][1]
    assert call_batch_id == batch_id


def test_upload_qid_batch_config_file_invalid_batch_id(client):
    # Given
    post_data = {'config-file': (BytesIO(b'config\nfile'), 'config-file.csv'), 'batch_id': 'not_a_valid_uuid4'}

    # When
    generate_messages_from_config_file_patch, response = post_to_generate_qid_batch(client, post_data)

    # Then
    assert response.status_code == 400
    assert b'Invalid UUID for batch ID' in response.data


def test_upload_qid_batch_no_config_file(client):
    # Given
    post_data = {'batch_id': ''}

    # When
    generate_messages_from_config_file_patch, response = post_to_generate_qid_batch(client, post_data)

    # Then
    assert response.status_code == 400
    assert b'No config file selected' in response.data


def post_to_generate_qid_batch(client, data):
    with patch('app.views.generate_qid_batch.generate_messages_from_config_file') as patched_generate:
        response = client.post('/generate-qid-batch', data=data)
    return patched_generate, response
