from sqlalchemy import create_engine

from main.cfg.local import config
from main.models.base import Base
from main.models.user import User
from main.models.blog import Blog
from main.models.like import Like

engine = create_engine(config.MYSQL_URL)

Base.metadata.create_all(engine)
