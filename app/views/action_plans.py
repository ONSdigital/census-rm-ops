from flask import Blueprint, request, render_template
import jwt
import requests
import os

blueprint = Blueprint('action_plans', __name__, template_folder='templates')

IAP_AUDIENCE = os.environ['IAP_AUDIENCE']

def get_iap_user():
    iap_jwt = request.headers['x-goog-iap-jwt-assertion']
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=IAP_AUDIENCE)
    return decoded_jwt['email'], decoded_jwt

def get_jwt():
    iap_jwt = request.headers['x-goog-iap-jwt-assertion']
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=IAP_AUDIENCE)
    return decoded_jwt


def get_iap_public_key(key_id):
    if key_id not in get_iap_public_key.cache:
        resp = requests.get('https://www.gstatic.com/iap/verify/public_key')
        resp.raise_for_status()
        get_iap_public_key.cache = resp.json()

    return get_iap_public_key.cache[key_id], ''


get_iap_public_key.cache = {}

@blueprint.route('/', methods=['GET'])
def index():
    user = get_iap_user()
    jwt = get_jwt()

    return render_template(
        'main.html',
        user=user,
        jwt=jwt,
    )
