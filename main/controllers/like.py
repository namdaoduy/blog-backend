from flask import jsonify

from main import app, errors
from main.libs.auth import authorization
from main.libs.database import db
from main.models.blog import Blog
from main.models.like import Like


@app.route('/likes/<int:blog_id>', methods=['POST'])
@authorization
def like_blog(user_id, blog_id):
    liking_blog = db.session.query(Blog).filter_by(id=blog_id).first()
    if liking_blog is None:
        raise errors.NotFound()
    existed_like = db.session.query(Like).filter_by(blog_id=blog_id, user_id=user_id).first()
    if existed_like is not None:
        raise errors.LikeExisted()
    like = Like(user_id=user_id, blog_id=blog_id)
    db.session.add(like)
    db.session.commit()
    return jsonify(success=True)
