from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_email = db.Column(db.String(25), primary_key = True)
    user_password = db.Column(db.String(10))
    role = db.Column(db.String(10), default='user')