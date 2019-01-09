from flask import jsonify

from main import app
from main.libs.dbsession import DBSession
from main.models.blog import Blog


# paging
@app.route('/blogs')
def get_all_blogs():
    session = DBSession()
    blogs = session.query(Blog).order_by(Blog.created_at.desc()).all()
    # use schema
    return jsonify(success=True, data=[b.serialize for b in blogs])


@app.route('/blogs/<int:blog_id>', methods=['GET'])
def get_blog_by_id(blog_id):
    session = DBSession()
    blog = session.query(Blog).filter_by(id=blog_id).first()
    return jsonify(success=True, data=blog.serialize)


# use param
@app.route('/blogs/trending')
def get_trending_blogs():
    session = DBSession()
    # use CONSTANT for limit
    blogs = session.query(Blog).order_by(Blog.like.desc()).limit(3).all()
    return jsonify(success=True, data=[b.serialize for b in blogs])

# use HTTP code instead of success = True
