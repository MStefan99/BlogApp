from email_template import get_email_text
from mailer import *

# WARNING! Disabling email is used only during development process! ALWAYS TURN EMAIL ON BEFORE DEPLOYMENT!
EMAIL_ENABLED = True
SMTP_ADDRESS = '192.168.1.8'
SMTP_PORT = 3598


def send_mail(address, username, link, template):
    if EMAIL_ENABLED:
        message = Message(From="noreply@mstefan99.com", To=address)
        message.Subject, message.Html = get_email_text(username, link, template)

        sender = Mailer(SMTP_ADDRESS, SMTP_PORT)
        sender.send(message)

