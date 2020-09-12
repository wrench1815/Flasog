import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flasog import app, db, bcrypt, mail
from flasog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flasog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image, ImageOps
from flask_mail import Message


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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)
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
        flash('Account created Successfully! You can now Login.', 'success')
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
    flash('You have been Successfully Logged out.', 'success')
    return redirect(url_for('home'))


# function to save uploaded Profile Picture on server
# after scaling it down to 100x100
def save_profile_picture(form_profile_picture):
    random_hex = secrets.token_hex(8)
    _, pp_ext = os.path.splitext(form_profile_picture.filename)
    pp_name = random_hex + pp_ext
    pp_path = os.path.join(app.root_path, 'static/profileImages', pp_name)

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


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html',
                           title='posts by ' + user.username,
                           posts=posts,
                           user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@admin.flasog.com',
                  recipients=[user.email])
    msg.body = '''To reset your Password visit the following link:
{}

If your did not make this request then simply ignore this message and no changes will be made to your account.
'''.format(url_for('reset_token', token=token, _external=True))
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password',
            'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',
                           title='Reset Passord',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an Invalid or Expired Token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data)
        user.password = hashedPassword
        db.session.commit()
        flash('Password has been updated! You can now Login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form)


# 404 error handling route
@app.errorhandler(404)
def NotFound(e):
    return render_template('404.html', title='404 not Found')
