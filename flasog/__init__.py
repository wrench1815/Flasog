from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
import os
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY'
) or 'd4121fbc66d4bf9370ea11890096d19e72a544a7aa11e53c4fe2299dc5a84f5c'
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER',
                                           'smtp.googlemail.com')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT', '587')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True')
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
