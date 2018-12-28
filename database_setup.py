from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  email = Column(String(250), nullable=False)
  picture = Column(String(250), nullable=False)


class Blog(Base):
  __tablename__ = 'blogs'

  id = Column(Integer, primary_key=True)
  title = Column(String(250), nullable=False)
  body = Column(String(250), nullable=False)
  like = Column(Integer, default=0)
  createdAt = Column(DateTime, server_default=func.now())
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship(User)

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'title': self.title,
      'id': self.id,
      'body': self.body,
      'createAt': self.createdAt,
    }

engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/just_blog')

Base.metadata.create_all(engine)
