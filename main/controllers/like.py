from flask import jsonify

from main import app
from main.libs.auth import authorization
from main.libs.database import db
from main.models.like import Like


# write another decorator to check valid blog
@app.route('/likes/<int:blog_id>', methods=['POST'])
@authorization
def like_blog(user_id, blog_id):
    # check if liked? before add like
    like = Like(user_id=user_id, blog_id=blog_id)
    db.session.add(like)
    db.session.commit()
    return jsonify(success=True)