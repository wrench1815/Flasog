from flask import Blueprint, render_template, request
from flasog.models import Post

main = Blueprint('main', __name__)


# Home page route
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')


# about page route
@main.route('/about')
def about():
    return render_template('about.html', title='About me')


# contact page route
@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact me')
