import json
from celery import Celery
from conversion import convert
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect, render_template, request, url_for
from smtplib import SMTP


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
with open('config.json') as f:
    app.config.update(json.load(f))
celery = make_celery(app)


@celery.task()
def send_message(body, target):
    with open('config.json', 'r') as f:
        email_config = json.load(f)['email']
        server = SMTP(email_config['server'], email_config['port'])
        my_addr = email_config['user']
        pswd = email_config['password']

    # Log in to the server
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(my_addr, pswd)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'TextReminder'
    msg['From'] = my_addr
    msg['To'] = target
    msg.attach(MIMEText(body))
    server.send_message(msg)
    server.quit()


@app.route('/')
def main():
    with open('gateways.json') as f:
        gateways = json.load(f)
    return render_template('index.html',
                           entries=sorted(gateways.keys()))


@app.route('/task', methods=['POST'])
def register_task():
    form = request.form
    target = convert(form['number'], form['carrier'])
    send_message(form['message'], target)
    return redirect(url_for('main'))
