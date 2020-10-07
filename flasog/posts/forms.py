from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    post_title = StringField('Title', validators=[DataRequired()])
    # post_featured_image = FileField(
    #     'Featured Image',
    #     validators=[DataRequired(),
    #                 FileAllowed(['png', 'jpg', 'svg'])])
    post_content = PageDownField('Write Something',
                                 validators=[DataRequired()])
    post_category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Post')
