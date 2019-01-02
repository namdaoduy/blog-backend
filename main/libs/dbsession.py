from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.cfg.local import config
from main.models.base import Base

engine = create_engine(config.MYSQL_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
