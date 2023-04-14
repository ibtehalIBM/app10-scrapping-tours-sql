import smtplib
from email.message import EmailMessage
import imghdr

SENDER = ""
RECEIVER = ""
PASSWORD = ""


def send_email(msg):
    message = EmailMessage()
    message['Subject'] = 'New event was found'
    message.set_content(msg)

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, message.as_string())
    gmail.quit()


if __name__ == '__main__':
    send_email('New event was found')
