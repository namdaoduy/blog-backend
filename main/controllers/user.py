from flask import request, jsonify

from main import app
from main.libs.auth import authorization
from main.libs.dbsession import DBSession
from main.models.blog import Blog
from main.schemas.user import BlogSchema


@app.route('/user/blogs/<int:user_id>', methods=['GET'])
def get_blogs_by_user(user_id):
    session = DBSession()
    blogs = session.query(Blog).filter_by(user_id=user_id).all()
    return jsonify(success=True, data=[b.serialize for b in blogs])


@app.route('/blog', methods=['POST'])
@authorization
def post_blog(user_id):
    schema = BlogSchema()
    req = schema.load(request.get_json())
    if req.errors is not None:
        return jsonify(req.errors)
    session = DBSession()
    new_blog = Blog(title=req.title, body=req.body, user_id=user_id)
    session.add(new_blog)
    session.commit()
    return jsonify(success=True)


@app.route('/blog/<int:id>', methods=['PUT'])
@authorization
def put_blog(user_id, id):
    schema = BlogSchema()
    req = schema.load(request.get_json())
    if req.errors is not None:
        return jsonify(req.errors)
    session = DBSession()
    edit_blog = session.query(Blog).filter_by(id=id, user_id=user_id).first()
    if edit_blog is None:
        return jsonify(error=True)
    edit_blog.title = req.title
    edit_blog.body = req.body
    session.commit()
    return jsonify(success=True)


@app.route('/blog/<int:id>', methods=['DELETE'])
@authorization
def delete_blog(user_id, id):
    session = DBSession()
    deleting_blog = session.query(Blog).filter_by(user_id=user_id, id=id).first()
    if deleting_blog is None:
        return jsonify(error=True)
    session.delete(deleting_blog)
    session.commit()
    return jsonify(success=True)
