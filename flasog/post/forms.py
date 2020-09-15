from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    post_title = StringField('Title', validators=[DataRequired()])
    # post_featured_image = FileField(
    #     'Featured Image',
    #     validators=[DataRequired(),
    #                 FileAllowed(['png', 'jpg', 'svg'])])
    post_content = TextAreaField('Write Something',
                                 validators=[DataRequired()])
    post_category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Post')
