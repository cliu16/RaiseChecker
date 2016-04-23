#!/usr/bin/python

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host="smtp.gmail.com"
mail_user=""
mail_pass=""

sender = ""
receivers = []

def init(m_user, m_pass):
    mail_user=m_user
    mail_pass=m_pass
    sender = mail_user+'@gmail.com'
    receivers.append(sender)
    
def sendMsg(subject, msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("Raise Discount Alert", 'utf-8')
    message['To'] =  Header("Chen", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Email send successfully!"
        smtpObj.close()
    except smtplib.SMTPException:
        print "Error: Can not send email!"
