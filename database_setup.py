from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  email = Column(String(250), nullable=False)
  picture = Column(String(250), nullable=False)


class Blog(Base):
  __tablename__ = 'blog'

  id = Column(Integer, primary_key=True)
  title = Column(String(250), nullable=False)
  body = Column(String(250), nullable=False)
  createdAt = Column(DateTime(), nullable=False)
  user_id = Column(Integer, ForeignKey('user.id'))
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
