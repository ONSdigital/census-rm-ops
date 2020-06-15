from flask import Blueprint, request, render_template
from app.auth import auth
import jwt
import re
import os

blueprint = Blueprint('action_plans', __name__, template_folder='templates')

IAP_AUDIENCE = os.environ['IAP_AUDIENCE']

def get_iap_user():
    iap_jwt = request.headers['x-goog-iap-jwt-assertion']
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=IAP_AUDIENCE)
    return decoded_jwt['email']


def get_iap_public_key(key_id):
    if key_id not in get_iap_public_key.cache:
        resp = request.get('https://www.gstatic.com/iap/verify/public_key')
        resp.raise_for_status()
        get_iap_public_key.cache = resp.json()

    return get_iap_public_key.cache[key_id]


get_iap_public_key.cache = {}

@blueprint.route('/', methods=['GET'])
@auth.login_required
def index():
    user = get_iap_user()

    return render_template(
        'main.html',
        user=user,
    )
