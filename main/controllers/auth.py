import datetime
import json

import httplib2
import jwt
from flask import request, make_response

from main import app
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
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps({'error': 'Wrong user'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != config.GOOGLE_CLIENT_ID:
        response = make_response(json.dumps({'error': 'Wrong app'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    user = db.session.query(User).filter_by(id=profile['googleId']).first()
    if user is None:
        new_user = User(id=profile['googleId'],
                        name=profile['name'],
                        picture=profile['imageUrl'],
                        email=profile['email'])
        db.session.add(new_user)
        db.session.commit()

    access_token = jwt.encode({
        'user_id': gplus_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
    }, config.JWT_SECRET_KEY, algorithm='HS256')

    response = make_response(AccessTokenSchema().jsonify({
        'user_id': gplus_id,
        'access_token': access_token
    }), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
