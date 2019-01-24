from flask import jsonify, request
from marshmallow import ValidationError

from main import app
from main import errors
from main import config
from main.libs.auth import authorization, optional_auth
from main.libs.database import db
from main.models.blog import Blog
from main.models.like import Like
from main.schemas.blog import BlogSchema


@app.route('/blogs')
def get_all_blogs():
    page = int(request.args.get('page') or 1)
    blogs_page = db.session.query(Blog)\
        .order_by(Blog.created_at.desc())\
        .paginate(page, config.BLOG_PAGING_LIMIT, error_out=False)
    blogs = blogs_page.items
    data = {
        'pagination': {
            'total': blogs_page.total,
            'offset': (blogs_page.page - 1) * blogs_page.per_page,
            'limit': blogs_page.per_page,
        },
        'blogs': [b.preview for b in blogs]
    }
    response = jsonify({
        'data': data,
        'success': True
    })
    return response


@app.route('/blogs/<int:blog_id>', methods=['GET'])
@optional_auth
def get_blog_by_id(user_id, blog_id):
    blog = db.session.query(Blog).filter_by(id=blog_id).first()
    is_liked = False
    if user_id is not None:
        existed_like = db.session.query(Like).filter_by(blog_id=blog_id, user_id=user_id).first()
        if existed_like is not None:
            is_liked = True
    blog.is_liked = is_liked
    response = BlogSchema().jsonify(blog.serialize)
    return response


# use param
@app.route('/blogs/trending')
def get_trending_blogs():
    blogs = db.session.query(Blog)\
        .order_by(Blog.like.desc())\
        .limit(config.BLOG_TRENDING_LIMIT)\
        .all()
    response = BlogSchema().jsonify((b.serialize for b in blogs), many=True)
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
