from flask import request, jsonify

from main import app
from main.libs.auth import authorization
from main.libs.database import db
from main.models.blog import Blog
from main.models.like import Like
from main.models.user import User
from main.schemas.blog import BlogSchema
from main.schemas.user import UserSchema


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is None:
        return jsonify(error=True)
    schema = UserSchema()
    return schema.jsonify(user)


@app.route('/users/<int:user_id>/blogs', methods=['GET'])
def get_blogs_by_user(user_id):
    blogs = db.session.query(Blog).filter_by(user_id=user_id).all()
    return jsonify(success=True, data=[b.serialize for b in blogs])


# move to blog.py
@app.route('/blogs', methods=['POST'])
@authorization
def post_blog(user_id):
    schema = BlogSchema()
    # req name??
    req = schema.load(request.get_json())
    if len(req.errors) > 0:
        #
        return jsonify(req.errors)
    new_blog = Blog(title=req.data["title"], body=req.data["body"], user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(success=True)


@app.route('/blogs/<int:blog_id>', methods=['PUT'])
@authorization
def put_blog(user_id, blog_id):
    schema = BlogSchema()
    req = schema.load(request.get_json())
    if len(req.errors) > 0:
        return jsonify(req.errors)
    edit_blog = db.session.query(Blog).filter_by(id=blog_id, user_id=user_id).first()
    if edit_blog is None:
        # Which error? action prohibit or blog not found??
        return jsonify(error=True)
    # use '' for all, not ""
    edit_blog.title = req.data["title"]
    edit_blog.body = req.data["body"]
    db.session.commit()
    return jsonify(success=True)


@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
@authorization
def delete_blog(user_id, blog_id):
    deleting_blog = db.session.query(Blog).filter_by(user_id=user_id, id=blog_id).first()
    if deleting_blog is None:
        return jsonify(error=True)
    db.session.delete(deleting_blog)
    db.session.commit()
    return jsonify(success=True)


# use likes, and POST instead of GET
# write another decorator to check valid blog
@app.route('/blogs/<int:blog_id>/like', methods=['GET'])
@authorization
def like_blog(user_id, blog_id):
    # check if liked? before add like
    like = Like(user_id=user_id, blog_id=blog_id)
    db.session.add(like)
    db.session.commit()
    return jsonify(success=True)
