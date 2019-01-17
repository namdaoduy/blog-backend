from main.libs.database import db


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(1000), db.ForeignKey('users.id', ondelete='CASCADE'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id', ondelete='CASCADE'))
