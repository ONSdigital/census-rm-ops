import json
import uuid
from unittest.mock import patch

import pytest

from app import create_app
from app.generate_qid_batch import generate_messages_from_config_file


@pytest.fixture(autouse=True)
def use_unit_test_config():
    app = create_app('UnitTestConfig')
    app.app_context().push()


def test_generate_messages_from_config_file_path_publishes_correct_quantities():
    # Given
    batch_id = uuid.uuid4()

    # When
    publish_message_call_list = generate_messages_with_mocked_rabbit(('"Questionnaire type","Quantity"\n',
                                                                      '"01","2"\n',
                                                                      '"02","1"'),
                                                                     batch_id)

    # Then
    assert json.loads(publish_message_call_list[0][0][0])['questionnaireType'] == '01'
    assert json.loads(publish_message_call_list[1][0][0])['questionnaireType'] == '01'
    assert json.loads(publish_message_call_list[2][0][0])['questionnaireType'] == '02'
    assert len(publish_message_call_list) == 3


def test_generate_messages_from_config_file_path_sets_batch_id():
    # Given
    batch_id = uuid.uuid4()

    # When
    publish_message_call_list = generate_messages_with_mocked_rabbit(('"Questionnaire type","Quantity"\n',
                                                                      '"01","2"\n',
                                                                      '"02","1"'),
                                                                     batch_id)

    # Then
    assert all(json.loads(message[0][0])['batchId'] == str(batch_id) for message in publish_message_call_list)


def generate_messages_with_mocked_rabbit(config_file, batch_id):
    with patch('app.generate_qid_batch.RabbitContext') as patch_rabbit:
        generate_messages_from_config_file(config_file, batch_id)
    return patch_rabbit.return_value.__enter__.return_value.publish_message.call_args_list
