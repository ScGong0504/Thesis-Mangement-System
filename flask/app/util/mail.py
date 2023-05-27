from flask_mail import Mail, Message
from flask import current_app
from threading import Thread


def send_mail(to, subject, body):
    mail = Mail(current_app)
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['MAIL_SUBJECT_SENDER'], recipients=[to])
    msg.body = str(body)
    thr = Thread(target=send_mail_async, args=(mail, msg, current_app._get_current_object()))
    thr.start()


def send_mail_async(mail, msg, app):
    with app.app_context():
        mail.send(msg)
