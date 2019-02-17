from email_template import get_text
import email.message
import smtplib

SMTP_ADDRESS = 'in-v3.mailjet.com'
SMTP_PORT = 587
SMTP_USERNAME = 'c6878f9f1439d09c4966715dc49577f1'
SMTP_PASSWORD = '3b02bb383693698006e94ed6d1b287f1'


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

