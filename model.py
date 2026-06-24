from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(25))
    user_name = db.Column(db.String())
    user_password = db.Column(db.String(10))
    role = db.Column(db.String(10), default='user')
    approved = db.Column(db.Boolean(), default=False)
    blacklisted = db.Column(db.Boolean(), default=False)

class Trek(db.Model):
    trek_id = db.Column(db.Integer(), primary_key=True)
    trek_name = db.Column(db.String(), unique=True)
    trek_status = db.Column(db.String(), default='active')
    trek_details = db.Column(db.Text(), nullable=True)
    responsible_trek_staff = db.Column(db.Integer,
                                       db.ForeignKey('user.user_id'),
                                       nullable=True)