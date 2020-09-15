from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flasog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flasog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flasog import bcrypt, db, app
from flasog.users.utils import save_profile_picture, send_reset_email

users = Blueprint('users', __name__)


# register page route
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


# login page route
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(
                url_for('main.home'))
        else:
            flash('Wrong Credentials! Check Email and Password and Try again.',
                  'danger')
    return render_template('login.html', title='Login', form=form)


# logout route
@users.route('/logout')
def logout():
    logout_user()
    flash('You have been Successfully Logged out.', 'success')
    return redirect(url_for('main.home'))


# account page route
@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.first_name.data, form.last_name.data, form.email.data, form.username.data = current_user.first_name, current_user.last_name, current_user.email, current_user.username
    imageFile = url_for('static',
                        filename='profileImages/' + current_user.profile_image)
    return render_template('account.html',
                           title='Account',
                           imageFile=imageFile,
                           form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html',
                           title='posts by ' + user.username,
                           posts=posts,
                           user=user)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
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
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            'An email has been sent with instructions to reset your password',
            'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Passord',
                           form=form)
