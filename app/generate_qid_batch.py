import csv
import json
import uuid

from flask import current_app

from app.rabbit_context import RabbitContext


def generate_messages_from_config_file(config_file, batch_id: uuid.UUID):
    config_file_reader = csv.DictReader(config_file)
    with RabbitContext(queue_name=current_app.config['RABBITMQ_UNADDRESSED_QID_QUEUE']) as rabbit:
        for row in config_file_reader:
            message_count = int(row['Quantity'])
            message_json = create_message_json(row['Questionnaire type'], batch_id)
            print(f'Queueing {message_count} questionnaire type {row["Questionnaire type"]}')
            for _ in range(message_count):
                rabbit.publish_message(message_json, 'application/json')


def create_message_json(questionnaire_type, batch_id: uuid.UUID):
    return json.dumps({'questionnaireType': questionnaire_type, 'batchId': str(batch_id)})
