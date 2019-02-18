from email_template import get_text
import email.message
import smtplib

EMAIL_ENABLED = True
SMTP_ADDRESS = '192.168.1.8'
SMTP_PORT = 3598


def send_mail(address, username, link, template):
    if EMAIL_ENABLED:
        smtp = smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT)

        msg = email.message.Message()
        msg['Subject'] = 'galera.dev registration'
        msg['From'] = 'noreply@mstefan99.com'
        msg['To'] = address
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(get_text(username, link, template=template))

        smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        smtp.close()

