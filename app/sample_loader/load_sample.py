import csv
import json
import os
import sys
import uuid
from typing import Iterable

import jinja2

from app.sample_loader.rabbit_context import RabbitContext
from app.sample_loader.redis_pipeline_context import RedisPipelineContext


def load_sample(sample_file: Iterable[str], collection_exercise_id: str, action_plan_id: str,
                collection_instrument_id: str):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    _load_sample_units(action_plan_id, collection_exercise_id, collection_instrument_id, sample_file_reader)


def _load_sample_units(action_plan_id: str, collection_exercise_id: str, collection_instrument_id: str,
                       sample_file_reader: Iterable[str]):
    case_message_template = jinja2.Environment(
        loader=jinja2.FileSystemLoader([os.path.dirname(__file__)])).get_template('message_template.xml')
    with RabbitContext() as rabbit, RedisPipelineContext() as redis_pipeline:
        print(f'Loading sample units to queue {rabbit.queue_name}')
        for count, sample_row in enumerate(sample_file_reader):
            sample_unit_id = uuid.uuid4()
            rabbit.publish_message(
                message=case_message_template.render(sample=sample_row,
                                                     sample_unit_id=sample_unit_id,
                                                     collection_exercise_id=collection_exercise_id,
                                                     action_plan_id=action_plan_id,
                                                     collection_instrument_id=collection_instrument_id),
                content_type='text/xml')
            sample_unit = {
                f'sampleunit:{sample_unit_id}': _create_sample_unit_json(sample_unit_id, sample_row)}
            redis_pipeline.set_names_to_values(sample_unit)

            if count % 5000 == 0:
                sys.stdout.write(f'\r{count} sample units loaded')
                sys.stdout.flush()
    print(f'\nAll sample units have been added to the queue {rabbit.queue_name} and Redis')


def _create_sample_unit_json(sample_unit_id, sample_unit) -> str:
    sample_unit = {'id': str(sample_unit_id), 'attributes': sample_unit}
    return json.dumps(sample_unit)
