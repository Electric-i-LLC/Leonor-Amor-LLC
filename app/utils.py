import os
import secrets
import hashlib
from PIL import Image

from app import create_app, mail
from flask import make_response, request
from flask_mail import Mail, Message
from smtplib import SMTP, SMTP_SSL

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(create_app.root_path, 'static/img/db/products', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def delete_picture(form_picture):
	previous_picture = os.path.join(create_app.root_path, "static/img/db/products", form_picture)
	if os.path.exists(previous_picture) and form_picture != "default.jpg":
		os.remove(previous_picture)
    
	else:
		return False

	return True



def const_hash(data):
    hashed = str(int(hashlib.md5(data.encode('utf-8')).hexdigest(), 16))
    return hashed




def send_email(subject, sender, recipients, body, attachment_1=None, attachment_2=None, attachment_3=None):
    #try:
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body

    if attachment_1:
        picture_path = os.path.join(create_app.root_path, 'static/img/db/products', attachment_1)
        with open(picture_path, 'rb') as fp:
            if attachment_1[-3:] == 'png':
                msg.attach('image.png', 'image/png', fp.read())
            elif attachment_1[-3:] == 'jpg':
                msg.attach('image.jpg', 'image/jpg', fp.read())
            elif attachment_1[-4:] == 'jpeg':
                msg.attach('image.jpeg', 'image/jpeg', fp.read())

    if attachment_2:
        picture_path = os.path.join(create_app.root_path, 'static/img/db/products', attachment_2)
        with open(picture_path, 'rb') as fp:
            if attachment_2[-3:] == 'png':
                msg.attach('image.png', 'image/png', fp.read())
            elif attachment_2[-3:] == 'jpg':
                msg.attach('image.jpg', 'image/jpg', fp.read())
            elif attachment_2[-4:] == 'jpeg':
                msg.attach('image.jpeg', 'image/jpeg', fp.read())

    if attachment_3:
        picture_path = os.path.join(create_app.root_path, 'static/img/db/products', attachment_3)
        with open(picture_path, 'rb') as fp:
            if attachment_3[-3:] == 'png':
                msg.attach('image.png', 'image/png', fp.read())
            elif attachment_3[-3:] == 'jpg':
                msg.attach('image.jpg', 'image/jpg', fp.read())
            elif attachment_3[-4:] == 'jpeg':
                msg.attach('image.jpeg', 'image/jpeg', fp.read())
    mail.send(msg)

    return True

    #except:
    #    return False
