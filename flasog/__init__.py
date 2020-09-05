from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
# app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASOG_MAIL_SENDER'] = 'Flasog Admin'
app.config['FLASOG_ADMIN'] = os.environ.get('FLASOG_ADMIN')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # location to sql Database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'
bootstrap = Bootstrap(app)
mail = Mail(app)
migrate = Migrate(app, db)

from flasog import routes
