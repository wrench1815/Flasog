from datetime import datetime
from flasog import db, loginManager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@loginManager.user_loader
def LoadUser(UserId):
    return User.query.get(int(UserId))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(20),
                              nullable=False,
                              default='default.svg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.profile_image}')"

    def generate_confirmation_token(self, expiration=86400):
        """Generate Token for Confirmation"""

        token = Serializer(app.config['SECRET_KEY'], expiration)
        return token.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        """Check the Token for the data encoded"""

        token = Serializer(app.config['SECRET_KEY'])

        try:
            data = token.load(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    post_category = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
