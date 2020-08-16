from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fb66c54c92550f163e1307990d402d5b'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # location to sql Database
db = SQLAlchemy(app)

from flasog import routes
