from threading import Thread
from flask import render_template
from flask_mail import Message
from flasog import mail, app


def send_async_message(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message('Flasog' + ' ' + subject,
                  sender=app.config['FLASOG_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail_thrd = Thread(target=send_async_message, args=[app, msg])
    mail_thrd.start()
    return mail_thrd
