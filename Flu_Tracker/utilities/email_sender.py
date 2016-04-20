import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, subject, message):
    msg = MIMEMultipart('alternative')
    html = """\
    <html>
      <head></head>
      <body><b>user email: </b>""" + email + """<br/><b> user message: </b>""" + message + """/""" + """
      </body>
    </html>
    """

    message = MIMEText(html, 'html')
    msg.attach(message)
    msg['Subject'] = subject

    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('flutrakr@gmail.com','admin#password')
    mail.sendmail("flutrakr@gmail.com", 'daviddunnepc@gmail.com', msg.as_string())
    mail.close()