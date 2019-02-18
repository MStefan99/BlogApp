from email_template import get_text
import email.message
import smtplib

SMTP_ADDRESS = 'email-smtp.us-west-2.amazonaws.com'
SMTP_PORT = 587
SMTP_USERNAME = 'AKIAILKJYPL2KJUEH42Q'
SMTP_PASSWORD = 'BKodb/aRE+tSJXolb7DVRl4SU7CHqTP0aVeodr6pLDe0'


def send_mail(address, username, link, template):
    smtp = smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)

    msg = email.message.Message()
    msg['Subject'] = 'galera.dev registration'
    msg['From'] = 'noreply@mstefan99.com'
    msg['To'] = address
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(get_text(username, link, template=template))

    smtp.sendmail(msg['From'], [msg['To']], msg.as_string())

