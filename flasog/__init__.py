from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb66c54c92550f163e1307990d402d5b'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # location to sql Database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)

from flasog import routes
