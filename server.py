from flask import Flask, request, redirect, jsonify, url_for, make_response, abort
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Blog

import jwt
from functools import wraps

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import httplib2
import requests
import datetime

SECRET = json.loads(open('credentials.json', 'r').read())
CLIENT_ID = SECRET['web']['client_id']
APPLICATION_NAME = "just-blog-namdaoduy"
SECRET = "something"

engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/just_blog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def validate(fn):
  @wraps(fn)
  def wrapper(*args, **kwargs):
    if not 'Authorization' in request.headers:
      abort(401)
    user = None
    data = request.headers['Authorization'].encode('ascii','ignore')
    token = str.replace(str(data), 'Bearer ','')
    try:
      user = jwt.decode(token, SECRET, algorithms=['HS256'])['sub']
    except:
      abort(401)
    return fn(user, *args, **kws)
  return wrapper


@app.route('/test')
@validate
def testServer():
  response = make_response(json.dumps({'hello': 'hi'}), 200)
  response.headers['Content-Type'] = 'application/json'
  return response


@app.route('/login', methods=['POST'])
def login():
  credentials = request.get_json()
  
  # Check that the access token is valid.
  access_token = credentials['accessToken']
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
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
  if result['issued_to'] != CLIENT_ID:
    response = make_response(json.dumps({'error': 'Wrong app'}), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  encoded = jwt.encode({
    'id': credentials['profileObj']['googleId'],
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*24)
  }, SECRET, algorithm='HS256')

  response = make_response(json.dumps({
    'id': credentials['profileObj']['googleId'],
    'access_token': encoded
  }), 200)
  response.headers['Content-Type'] = 'application/json'
  return response

if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
