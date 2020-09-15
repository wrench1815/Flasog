from flasog import models
from flask_login import login_required, current_user
from flasog import db
from flasog.post.forms import PostForm
from flasog.models import Post
from flask import Blueprint, flash, redirect, url_for, render_template, abort, request

posts = Blueprint('posts', __name__)


# blog page route
@posts.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)
    return render_template('blog.html', title='Blog', posts=posts)


@posts.route('/blog/new', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.blog'))
    return render_template('create_new_post.html',
                           title='New Post',
                           form=form,
                           legend='New Post')


@posts.route('/blog/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/blog/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.post_title.data, form.post_content.data, form.post_category.data = post.title, post.content, post.post_category
    return render_template('create_new_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


@posts.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been Deleted!', 'success')
    return redirect(url_for('posts.blog'))
