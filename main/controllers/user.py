from flask import jsonify

from main import app
from main.libs.database import db
from main.models.blog import Blog
from main.models.user import User
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
