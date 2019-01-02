from flask import request, jsonify

from main import app
from main.libs.auth import authorization
from main.libs.dbsession import DBSession
from main.models.blog import Blog


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
