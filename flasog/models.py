from datetime import datetime
from flasog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    userEmail = db.Column(db.String(120), unique=True, nullable=False)
    userPassword = db.Column(db.String(60), nullable=False)
    userImage = db.Column(db.String(20), nullable=False, default='default.jpg')
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