from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from main.cfg.local import config

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String(1000), primary_key=True)
    name = Column(String(1000), nullable=False)
    email = Column(String(1000), nullable=False)
    picture = Column(String(1000), nullable=False)


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


engine = create_engine(config.MYSQL_URL)

Base.metadata.create_all(engine)
