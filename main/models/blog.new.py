from sqlalchemy import select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from main.libs.database import db
from main.models.like import Like
from main.models.user import User


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.String(1000), db.ForeignKey('users.id'))
    user = relationship(User)
    like = column_property(
        select([func.count(Like.id)]).where(Like.blog_id == id)
    )

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'like': self.like,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'author': self.user.name,
            'picture': self.user.picture
        }
