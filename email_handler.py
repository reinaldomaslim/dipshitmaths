import smtplib
import sys
sys.path.append('/home/rm/')
from password import PASS
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user = 'dipshitmaths@gmail.com'
gmail_password = PASS

sent_from = gmail_user
to = 'yanpaioo94@gmail.com'
path_to_pdf = '/home/rm/Documents/cs5330_randomized_algorithms/wk_1/week1.pdf'

msg = MIMEMultipart()
message = 'Send from Hostname: dipshit'
msg['Subject'] = 'dailytorture'
msg['From'] = sent_from
msg['To'] = to
msg.attach(MIMEText(message, "plain"))
with open(path_to_pdf, "rb") as f:
    attach = MIMEApplication(f.read(),_subtype="pdf")
attach.add_header('Content-Disposition','attachment',filename='problem set')
msg.attach(attach)


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
# server.sendmail(sent_from, to, email_text)
server.close()

print('Email sent!')
