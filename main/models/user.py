from main.libs.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(1000), primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(1000), nullable=False)
    picture = db.Column(db.String(1000), nullable=False)
