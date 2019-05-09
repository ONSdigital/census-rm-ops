import csv
import json
import sys
from typing import Iterable

from app.sample_loader.rabbit_context import RabbitContext


def load_sample(sample_file: Iterable[str], collection_exercise_id: str, action_plan_id: str):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    _load_sample_units(action_plan_id, collection_exercise_id, sample_file_reader)


def _load_sample_units(action_plan_id: str, collection_exercise_id: str, sample_file_reader: Iterable[str]):
    with RabbitContext() as rabbit:
        print(f'Loading sample units to queue {rabbit.queue_name}')
        for count, sample_row in enumerate(sample_file_reader):
            rabbit.publish_message(_create_case_json(sample_row, collection_exercise_id=collection_exercise_id,
                                                     action_plan_id=action_plan_id),
                                   content_type='application/json')

            if count % 5000 == 0:
                sys.stdout.write(f'\r{count} sample units loaded')
                sys.stdout.flush()
    print(f'\nAll sample units have been added to the queue {rabbit.queue_name}')


def _create_case_json(sample_row, collection_exercise_id, action_plan_id) -> str:
    create_case = {'arid': sample_row['ARID'], 'estabArid': sample_row['ESTAB_ARID'], 'uprn': sample_row['UPRN'],
                   'addressType': sample_row['ADDRESS_TYPE'], 'estabType': sample_row['ESTAB_TYPE'],
                   'addressLevel': sample_row['ADDRESS_LEVEL'], 'abpCode': sample_row['ABP_CODE'],
                   'organisationName': sample_row['ORGANISATION_NAME'],
                   'addressLine1': sample_row['ADDRESS_LINE1'], 'addressLine2': sample_row['ADDRESS_LINE2'],
                   'addressLine3': sample_row['ADDRESS_LINE3'], 'townName': sample_row['TOWN_NAME'],
                   'postcode': sample_row['POSTCODE'], 'latitude': sample_row['LATITUDE'],
                   'longitude': sample_row['LONGITUDE'], 'oa': sample_row['OA'],
                   'lsoa': sample_row['LSOA'], 'msoa': sample_row['MSOA'],
                   'lad': sample_row['LAD'], 'rgn': sample_row['RGN'],
                   'htcWillingness': sample_row['HTC_WILLINGNESS'], 'htcDigital': sample_row['HTC_DIGITAL'],
                   'treatmentCode': sample_row['TREATMENT_CODE'], 'collectionExerciseId': collection_exercise_id,
                   'actionPlanId': action_plan_id}
    return json.dumps(create_case)
