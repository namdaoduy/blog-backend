from sqlalchemy import Column, String
from main.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(1000), primary_key=True)
    name = Column(String(1000), nullable=False)
    email = Column(String(1000), nullable=False)
    picture = Column(String(1000), nullable=False)