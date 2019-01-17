import datetime
import json

import jwt
import requests
from flask import request

from main import app
from main import errors
from main.cfg.local import config
from main.libs.database import db
from main.models.user import User
from main.schemas.auth import AccessTokenSchema


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    access_token = credentials['accessToken']
    gplus_id = credentials['googleId']
    profile = credentials['profileObj']

    # Check that the access token is valid.
    url = (config.GOOGLE_TOKEN_VERIFY_STRING % access_token)
    resp = requests.get(url)
    if not resp.status_code == 200:
        raise errors.InvalidGoogleAccessToken()
    # If OK, load result content
    try:
        result = json.loads(resp.content)
    except ValueError:
        raise errors.InvalidGoogleAccessToken()

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        raise errors.InvalidGoogleAccessToken()

    # Verify that the access token is used for the intended user.
    if result['user_id'] != gplus_id:
        raise errors.Unauthorized()

    # Verify that the access token is valid for this app.
    if result['issued_to'] != config.GOOGLE_CLIENT_ID:
        raise errors.Unauthorized()

    # Check if user not found, create new one
    user = db.session.query(User).filter_by(id=profile['googleId']).first()
    if user is None:
        new_user = User(id=profile['googleId'],
                        name=profile['name'],
                        picture=profile['imageUrl'],
                        email=profile['email'])
        db.session.add(new_user)
        db.session.commit()

    # Make new access token
    access_token = jwt.encode({
        'user_id': gplus_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config.JWT_TIME_TO_LIVE)
    }, config.JWT_SECRET_KEY, algorithm='HS256')

    response = AccessTokenSchema().jsonify({
        'user_id': gplus_id,
        'access_token': access_token
    })
    return response
