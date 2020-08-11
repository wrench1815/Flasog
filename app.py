##################################
#  Author : Hardeep Kumar
#  Created On : Tue Aug 11 2020
#  File : app.py
#
#  Main file for Flasog
##################################
from flask import Flask, render_template

app = Flask(__name__)

posts = [{
    'author': 'Hardeep Kumar',
    'title': 'Blog Post 1',
    'content': 'First Post Content',
    'datePublished': '11 Aug, 2020'
}, {
    'author': 'Hardeep Kumar',
    'title': 'Blog Post 2',
    'content': 'Second Post Content',
    'datePublished': '11 Aug, 2020'
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


if __name__ == "__main__":
    app.run(debug=True)