import datetime
import json

import httplib2
import jwt
from flask import request, make_response

from main import app
from main.cfg.local import config
from main.libs.dbsession import DBSession
from main.models.user import User

from main.schemas.auth import AccessTokenSchema


@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()

    # Check that the access token is valid.
    access_token = credentials['accessToken']
    url = (config.GOOGLE_TOKEN_VERIFY_STRING % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials['googleId']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps({'error': 'Wrong user'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != config.GOOGLE_CLIENT_ID:
        response = make_response(json.dumps({'error': 'Wrong app'}), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    session = DBSession()
    profile = credentials['profileObj']
    user = session.query(User).filter_by(id=profile['googleId']).first()
    if user is None:
        new_user = User(id=profile['googleId'],
                        name=profile['name'],
                        picture=profile['imageUrl'],
                        email=profile['email'])
        session.add(new_user)
        session.commit()

    # varialble name nonsense
    access_token = jwt.encode({
        'user_id': credentials['profileObj']['googleId'],
        # use google_id variable
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
    }, config.JWT_SECRET_KEY, algorithm='HS256')

    response = make_response(AccessTokenSchema().jsonify({
        'user_id': credentials['profileObj']['googleId'],
        'access_token': access_token
    }), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
