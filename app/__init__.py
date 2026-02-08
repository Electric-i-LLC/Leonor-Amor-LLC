import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

load_dotenv()

create_app = Flask(__name__)

# Access environment variables
create_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
create_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
create_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
create_app.config['FERNET_KEY'] = os.getenv('FERNET_KEY')
create_app.config['ADMIN_ID'] = os.getenv('ADMIN_ID')

db = SQLAlchemy(create_app)
migrate = Migrate(create_app, db)
bcrypt = Bcrypt(create_app)
login_manager = LoginManager(create_app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Paste all model imports for database creation
from app.models import User, Message, Appointment

# Create Database
with create_app.app_context():
    db.create_all()



create_app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
create_app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
create_app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
create_app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
create_app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
create_app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(create_app)

from app import routes
