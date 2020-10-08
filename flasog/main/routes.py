from flask import Blueprint, current_app, render_template, send_from_directory
import os

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


@main.route('/favicon.ico')
def favicon():
    return current_app.send_static_file("favicon.ico")

@main.route('/admin')
def admin():
    return render_template('')
