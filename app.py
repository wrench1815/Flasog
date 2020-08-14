##################################
#  Author : Hardeep Kumar
#  Created On : Tue Aug 11 2020
#  File : app.py
#
#  Main file for Flasog
##################################
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fb66c54c92550f163e1307990d402d5b'

posts = [{
    'author': 'Hardeep Kumar',
    'title': 'Blog Post 1',
    'content': 'First Post Content',
    'datePublished': '11 Aug, 2020',
    'postCategory': 'Technology'
}, {
    'author': 'Hardeep Kumar',
    'title': 'Blog Post 2',
    'content': 'Second Post Content',
    'datePublished': '11 Aug, 2020',
    'postCategory': 'Technology'
}]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.errorhandler(404)
def NotFound(e):
    return render_template('404.html', title='404 not Found')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.userName.data } Successfully!',
              'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)