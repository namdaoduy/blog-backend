from sqlalchemy import Column, String, ForeignKey, Integer

from main.models.base import Base


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(1000), ForeignKey('users.id', ondelete='CASCADE'))
    blog_id = Column(Integer, ForeignKey('blogs.id', ondelete='CASCADE'))
