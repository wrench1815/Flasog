import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flasog import app, db, bcrypt
from flasog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flasog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image, ImageOps
from flasog.email import send_email


# Home page route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


# about page route
@app.route('/about')
def about():
    return render_template('about.html', title='About me')


# blog page route
@app.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', title='Blog', posts=posts)


# contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact me')


# register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        send_email(app.config['FLASOG_ADMIN'],
                   'New User Sign UP',
                   'email/new_user',
                   user=form.username.data)
        token = user.generate_confirmation_token()
        send_email(user.email,
                   'Confirm Your Account',
                   'email/confirm',
                   user=user,
                   token=token)
        flash(
            'A Confirmation Email was sent Successfully. Please Verify your Email to Login!',
            'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(
                url_for('home'))
        else:
            flash('Wrong Credentials! Check Email and Password and Try again.',
                  'danger')
    return render_template('login.html', title='Login', form=form)


# logout route
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been Successfully Loged out.', 'success')
    return redirect(url_for('home'))


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home'))
    elif current_user.confirm(token):
        db.session.commit()
        flash('Your account has been verified! Welcome to Flasog!', 'success')
        return redirect(url_for('home'))
    else:
        flash('The confirmation link is either invalid or has been expired.',
              'warning')
        return redirect(url_for('home'))


# function to save uploaded Profile Picture on server
# after scaling it down to 100x100
def save_profile_picture(form_profile_picture):
    random_hex = secrets.token_hex(8)
    _, pp_ext = os.path.splitext(form_profile_picture.filename)
    pp_name = random_hex + pp_ext
    pp_path = os.path.join(app.root_path, 'static/profileImages', pp_name)

    # output_size = (100, 100)
    # scaled_pp = Image.open(form_profile_picture)
    # scaled_pp.thumbnail(output_size)
    if pp_ext == '.svg':
        form_profile_picture.save(pp_path)
        return pp_name
    else:
        pp = Image.open(form_profile_picture)
        resized_pp = ImageOps.fit(pp, (100, 100))

        resized_pp.save(pp_path)
        return pp_name


# account page route
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture = save_profile_picture(form.profile_picture.data)
            current_user.profile_image = profile_picture
        current_user.first_name, current_user.last_name, current_user.username, current_user.email = form.first_name.data, form.last_name.data, form.username.data, form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data, form.last_name.data, form.email.data, form.username.data = current_user.first_name, current_user.last_name, current_user.email, current_user.username
    imageFile = url_for('static',
                        filename='profileImages/' + current_user.profile_image)
    return render_template('account.html',
                           title='Account',
                           imageFile=imageFile,
                           form=form)


@app.route('/blog/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.post_title.data,
                    content=form.post_content.data,
                    author=current_user,
                    post_category=form.post_category.data)
        db.session.add(post)
        db.session.commit()
        flash('Post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('create_new_post.html',
                           title='New Post',
                           form=form,
                           legend='New Post')


@app.route('/blog/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/blog/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def updatePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title, post.content, post.post_category = form.post_title.data, form.post_content.data, form.post_category.data
        db.session.commit()
        flash('The post has been updated Successfully!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.post_title.data, form.post_content.data, form.post_category.data = post.title, post.content, post.post_category
    return render_template('create_new_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


@app.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been Deleted!', 'success')
    return redirect(url_for('blog'))


# 404 error handling route
@app.errorhandler(404)
def NotFound(e):
    return render_template('404.html', title='404 not Found')
