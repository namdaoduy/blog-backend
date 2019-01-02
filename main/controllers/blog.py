from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from main.cfg.local import config
from main.models.base import Base
from main.models.blog import Blog

engine = create_engine(config.MYSQL_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


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

