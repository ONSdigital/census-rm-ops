import json
from unittest.mock import patch

from app import create_app
from app.generate_qid_batch import generate_messages_from_config_file


def test_generate_messages_from_config_file_path():
    # Given
    app = create_app('UnitTestConfig')
    app.app_context().push()
    config_file = ('"Questionnaire type","Quantity"\n',
                   '"01","2"\n',
                   '"02","1"')

    # When
    with patch('app.generate_qid_batch.RabbitContext') as patch_rabbit:
        generate_messages_from_config_file(config_file)

    # Then
    patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value
    publish_message_call_list = patch_rabbit_context.publish_message.call_args_list

    assert json.loads(publish_message_call_list[0][0][0])['questionnaireType'] == '01'
    assert json.loads(publish_message_call_list[1][0][0])['questionnaireType'] == '01'
    assert json.loads(publish_message_call_list[2][0][0])['questionnaireType'] == '02'
