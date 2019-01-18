from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main import errors
from main import config
from main.libs.auth import authorization
from main.libs.database import db
from main.models.blog import Blog
from main.schemas.blog import BlogSchema


@app.route('/blogs')
def get_all_blogs():
    page = request.args.get('page') or 1
    blogs_page = db.session.query(Blog)\
        .order_by(Blog.created_at.desc())\
        .paginate(page, config.BLOG_PAGING_LIMIT, error_out=False)
    blogs = blogs_page.items
    response = BlogSchema().jsonify(b.preview for b in blogs)
    return response


@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    blog = db.session.query(Blog).filter_by(id=blog_id).first()
    response = BlogSchema().jsonify(blog.serialize, many=False)
    return response


# use param
@app.route('/blogs/trending')
def get_trending_blogs():
    blogs = db.session.query(Blog)\
        .order_by(Blog.like.desc())\
        .limit(config.BLOG_TRENDING_LIMIT)\
        .all()
    response = BlogSchema().jsonify(b.serialize for b in blogs)
    return response


@app.route('/blogs', methods=['POST'])
@authorization
def post_blog(user_id):
    schema = BlogSchema()
    try:
        blog_valid = schema.load(request.get_json())
    except ValidationError:
        raise errors.InvalidInputBlog()
    new_blog = Blog(title=blog_valid.data["title"], body=blog_valid.data["body"], user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(success=True)


@app.route('/blogs/<int:blog_id>', methods=['PUT'])
@authorization
def put_blog(user_id, blog_id):
    schema = BlogSchema()
    try:
        blog_valid = schema.load(request.get_json())
    except ValidationError:
        raise errors.InvalidInputBlog()
    edit_blog = db.session.query(Blog).filter_by(id=blog_id).first()
    if edit_blog is None:
        raise errors.NotFound()
    if edit_blog.user_id != user_id:
        raise errors.PermissionDenied()
    edit_blog.title = blog_valid.data['title']
    edit_blog.body = blog_valid.data['body']
    db.session.commit()
    return jsonify(success=True)


@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
@authorization
def delete_blog(user_id, blog_id):
    deleting_blog = db.session.query(Blog).filter_by(id=blog_id).first()
    if deleting_blog is None:
        raise errors.NotFound()
    if deleting_blog.user_id != user_id:
        raise errors.PermissionDenied()
    db.session.delete(deleting_blog)
    db.session.commit()
    return jsonify(success=True)
