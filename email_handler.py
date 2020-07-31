import os
import smtplib
import sys
sys.path.append('/home/rm/')
from password import PASS
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailHandler:

    def __init__(self, username, password):
        self._server_username = username
        self._server_password = password

    def send_email(self, dst_email, text, attachment):
        assert os.path.isfile(attachment)

        msg = MIMEMultipart()
        msg['Subject'] = 'Problem of the Week'
        msg['From'] = self._server_username
        msg['To'] = dst_email

        msg.attach(MIMEText(text, "plain"))
        with open(attachment, "rb") as f:
            attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename='problem set')
        msg.attach(attach)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(self._server_username, self._server_password)
        server.send_message(msg)
        server.close()

        print('Email sent!')


if __name__ == "__main__":
    emailHandler = EmailHandler('dipshitmaths@gmail.com', PASS)

    dst_email = 'reinaldomaslim@gmail.com'
    text = 'Hi fellow dipshits, \n\nThis is your problem of the week. \nGive your best and may the force be with you. \n\nHave a great day!'
    attachment = '/home/rm/Documents/dipshitmaths/latex/o_maths/0_qn.pdf'

    emailHandler.send_email(dst_email, text, attachment)
