from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_email = db.Column(db.String(25), primary_key = True)
    user_password = db.Column(db.String(10))
    role = db.Column(db.String(10), default='user')

class Trek(db.Model):
    trek_id = db.Column(db.Integer(), primary_key=True, autoincrement = True)
    trek_name = db.Column(db.String())
    trek_status = db.Column(db.String(), default='active')