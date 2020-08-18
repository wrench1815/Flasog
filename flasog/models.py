from datetime import datetime
from flasog import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def LoadUser(UserId):
    return User.query.get(int(UserId))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    userEmail = db.Column(db.String(120), unique=True, nullable=False)
    userPassword = db.Column(db.String(60), nullable=False)
    userImage = db.Column(db.String(20), nullable=False, default='default.svg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.userName}','{self.userEmail}','{self.userImage}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    datePosted = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.datePosted}')"