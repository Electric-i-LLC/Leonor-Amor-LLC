from app import db, login_manager

# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from flask import current_app
from flask_login import UserMixin


# Login by user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key =True)

    # Encrypted for security
    email  = db.Column(db.String(128), unique =True, nullable =True)
    phone = db.Column(db.String(128), unique =True, nullable =True)
    username  = db.Column(db.String(128), unique =True, nullable =True)

    # Hashed for speedy search
    email_hash    = db.Column(db.String(128), unique =True, nullable =True)
    phone_hash    = db.Column(db.String(128), unique =True, nullable =True)
    username_hash   = db.Column(db.String(128), unique =True, nullable =True)

    password    = db.Column(db.String(128), unique =True, nullable =True)

    admin    = db.Column(db.Boolean, nullable =False, default =False)
    profile_picture = db.Column(db.String(128), nullable =False)

    created         = db.Column(db.DateTime, nullable =False, default =datetime.utcnow)
    last_login      = db.Column(db.DateTime, nullable =True)
    last_seen       = db.Column(db.DateTime, nullable =True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title       = db.Column(db.String(128), nullable =False)
    description = db.Column(db.Text, nullable =False)

    status = db.Column(db.String(128), nullable =False, default ="UNOPENED")
    message_type = db.Column(db.String(128), nullable =True)

    deleted_from_sender = db.Column(db.Boolean, nullable =False, default =False)
    deleted_from_receiver = db.Column(db.Boolean, nullable =False, default =False)

    created = db.Column(db.DateTime, nullable =False, default =datetime.utcnow())

    gallery_1 = db.Column(db.String(128), nullable =True)
    gallery_2 = db.Column(db.String(128), nullable =True)
    gallery_3 = db.Column(db.String(128), nullable =True)
    video     = db.Column(db.String(128), nullable =True)


    sender        = db.Column(db.Integer, db.ForeignKey("user.id"), nullable =False)
    receiver      = db.Column(db.Integer, db.ForeignKey("user.id"), nullable =False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selected_datetime = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    whatsapp = db.Column(db.Boolean, default=False)
    telegram = db.Column(db.Boolean, default=False)
    signal = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




























'''
>>> from app import create_app, db, models
>>> create_app.app_context().push()
>>> db.create_all()
'''
