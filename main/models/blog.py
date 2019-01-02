from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from main.models.base import Base
from main.models.user import User


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    title = Column(String(1000), nullable=False)
    body = Column(Text, nullable=False)
    like = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(String(1000), ForeignKey('users.id'))
    user = relationship(User)

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