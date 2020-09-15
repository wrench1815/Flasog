from PIL import Image, ImageOps
from flask_mail import Message
from flasog import mail
import secrets
import os
from flasog import app
from flask import url_for


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@admin.flasog.com',
                  recipients=[user.email])
    msg.body = '''To reset your Password visit the following link:
{}

If your did not make this request then simply ignore this message and no changes will be made to your account.
'''.format(url_for('users.reset_token', token=token, _external=True))
    mail.send(msg)
