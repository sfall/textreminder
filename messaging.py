import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


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
