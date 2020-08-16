from flask import render_template, url_for, flash, redirect
from flasog import app, db, bcrypt
from flasog.forms import RegistrationForm, LoginForm
from flasog.models import User, Post

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
    return render_template('about.html', title='About me')


@app.route('/blog')
def blog():
    return render_template('blog.html', title='Blog')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact me')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.userPassword.data)
        user = User(userName=form.userName.data,
                    userEmail=form.userEmail.data,
                    userPassword=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash('Account Created Successfully! You can now Log In.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.userEmail.data == 'hk@flasog.com' and form.userPassword.data == 'admin':
            flash('Logged in Successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Wrong Credentials! Check Email and Password and Try again.',
                  'danger')
    return render_template('login.html', title='Login', form=form)


@app.errorhandler(404)
def NotFound(e):
    return render_template('404.html', title='404 not Found')