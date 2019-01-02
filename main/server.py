import datetime
import json

import httplib2
import jwt
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Blog
from main.cfg.local import config
from main.libs.auth import authorization

app = Flask(__name__)
CORS(app)

engine = create_engine(config.MYSQL_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/test')
@authorization
def test_server(user_id):
    response = make_response(json.dumps({'hello': user_id}), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


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

    encoded = jwt.encode({
        'user_id': credentials['profileObj']['googleId'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
    }, config.JWT_SECRET_KEY, algorithm='HS256')

    response = make_response(json.dumps({
        'user_id': credentials['profileObj']['googleId'],
        'access_token': encoded
    }), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/blogs')
def get_all_blogs():
    session = DBSession()
    blogs = session.query(Blog).all()
    return jsonify(success=True, data=[b.serialize for b in blogs])


@app.route('/blog/<int:id>', methods=['GET'])
def get_blog_by_id(id):
    session = DBSession()
    blog = session.query(Blog).filter_by(id=id).first()
    return jsonify(success=True, data=blog.serialize)


@app.route('/user/blogs/<int:user_id>', methods=['GET'])
def get_blogs_by_user(user_id):
    session = DBSession()
    blogs = session.query(Blog).filter_by(user_id=user_id).all()
    return jsonify(success=True, data=[b.serialize for b in blogs])


@app.route('/blog', methods=['POST'])
@authorization
def post_blog(user_id):
    req = request.get_json()
    title = req['title']
    body = req['body']
    if title is None or body is None:
        return jsonify(success=False)
    session = DBSession()
    new_blog = Blog(title=title, body=body, user_id=user_id)
    session.add(new_blog)
    session.commit()
    return jsonify(success=True)


@app.route('/blog/<int:id>', methods=['PUT'])
@authorization
def put_blog(user_id, id):
    req = request.get_json()
    title = req['title']
    body = req['body']
    session = DBSession()
    edit_blog = session.query(Blog).filter_by(id=id, user_id=user_id).first()
    edit_blog.title = title
    edit_blog.body = body
    session.commit()
    return jsonify(success=True)


@app.route('/blog/<int:id>', methods=['DELETE'])
@authorization
def delete_blog(user_id, id):
    session = DBSession()
    deleting_blog = session.query(Blog).filter_by(user_id=user_id, id=id).first()
    session.delete(deleting_blog)
    session.commit()
    return jsonify(success=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
