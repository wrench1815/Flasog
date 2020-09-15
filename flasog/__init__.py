from flasog.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
mail = Mail(app)

from flasog.main.routes import main
from flasog.users.routes import users
from flasog.post.routes import posts

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)
