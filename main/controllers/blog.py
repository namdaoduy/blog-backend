from flask import jsonify

from main import app
ç
from main.models.blog import Blog


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

