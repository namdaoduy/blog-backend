from flask_sqlalchemy import SQLAlchemy

from main import app
from main.cfg.local import config

app.config['SQLALCHEMY_DATABASE_URI'] = config.MYSQL_URL
db = SQLAlchemy(app)