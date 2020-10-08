from flasog.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_admin import Admin

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'
bootstrap = Bootstrap()
migrate = Migrate()
mail = Mail()
pagedown = PageDown()
admin = Admin(name='Flasog Admin', template_mode='bootstrap3')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    pagedown.init_app(app)
    admin.init_app(app)

    from flasog.main.routes import main
    from flasog.users.routes import users
    from flasog.posts.routes import posts
    from flasog.errors.error_handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    admin_views()
    return app


def admin_views():
    """
        Views for Admin Panel
    """

    from flask_admin.contrib.sqla import ModelView
    from flasog.models import User, Post

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
