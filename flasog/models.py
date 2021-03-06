from datetime import datetime
from flask import current_app
from flasog import db, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach


@loginManager.user_loader
def LoadUser(UserId):
    return User.query.get(int(UserId))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), default='user')
    profile_image = db.Column(db.String(20),
                              nullable=False,
                              default='default.svg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.profile_image}','{self.role}')"

    def get_reset_token(self, expires_sec=86400):
        """
            Generate Token for Password Reset
        """

        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
            verify Reset Token
        """

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads((token))['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_html = db.Column(db.Text)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    post_category = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
            'img', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4',
            'h5', 'p'
        ]
        target.content_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'),
                         tags=allowed_tags,
                         strip=True))

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


db.event.listen(Post.content, 'set', Post.on_changed_body)
