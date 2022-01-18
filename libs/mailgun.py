import os
from typing import List
from requests import Response, post
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from libs.strings import gettext   #this is called abosolute import
# from .strings import gettext   #this is called relative import

class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)  #super class allows you to give your extension a custo name



class GoogleMail:
    
    @classmethod
    def send_mail( cls, name, email, message):
        # set up the SMTP server
        s = smtplib.SMTP(host=os.environ.get("GOOGLE_SERVER"), port=os.environ.get("GOOGLE_SERVER_PORT"))
        # start smtp using tls
        s.starttls()
        # log into your account
        s.login(os.environ.get("MY_ADDRESS"), os.environ.get("PASSWORD"))
        

        msg = MIMEMultipart()       
        
        # setup the parameters of the message
        msg['From']= os.environ.get("MY_NAME")
        msg['To']=email
        msg['Subject']=os.environ.get("SUBJECT")
        # send the message via the server set up earlier.
        msg.attach(MIMEText(message, 'plain'))
        try:
            s.send_message(msg)
            s.quit()
            if True:
                print('email sent successfully ✓✓')       
        except:
            return (r'Failed sending email to:{} with address:{}'.format(name,email))
        del msg

    @classmethod
    def send_payment_alert( cls, name, email, message):
        # set up the SMTP server
        s = smtplib.SMTP(host=os.environ.get("GOOGLE_SERVER"), port=os.environ.get("GOOGLE_SERVER_PORT"))
        # start smtp using tls
        s.starttls()
        # log into your account
        s.login(os.environ.get("MY_ADDRESS"), os.environ.get("PASSWORD"))
        

        msg = MIMEMultipart()       
        
        # setup the parameters of the message
        msg['From']= os.environ.get("MY_NAME")
        msg['To']=email
        msg['Subject']=os.environ.get("PAYMENT_SUBJECT")
        # send the message via the server set up earlier.
        msg.attach(MIMEText(message, 'plain'))
        try:
            s.send_message(msg)
            s.quit()
            if True:
                print('email sent successfully ✓✓')       
        except:
            return (r'Failed sending email to:{} with address:{}'.format(name,email))
        del msg
        
    
    @classmethod
    def send_password_alert( cls, name, email, message):
        # set up the SMTP server
        s = smtplib.SMTP(host=os.environ.get("GOOGLE_SERVER"), port=os.environ.get("GOOGLE_SERVER_PORT"))
        # start smtp using tls
        s.starttls()
        # log into your account
        s.login(os.environ.get("MY_ADDRESS"), os.environ.get("PASSWORD"))

        msg = MIMEMultipart()       

        # setup the parameters of the message
        msg['From']= os.environ.get("MY_NAME")
        msg['To']=email
        msg['Subject']=os.environ.get("PASSWORD_SUBJECT")
        # send the message via the server set up earlier.
        msg.attach(MIMEText(message, 'plain'))
        try:
            s.send_message(msg)
            s.quit()
            if True:
                print('email sent successfully ✓✓')       
        except:
            return (r'Failed sending email to:{} with address:{}'.format(name,email))
        del msg


# In order to send a general email by calling send email
class Mailgun:
    #this is a way of securing our credential
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    FROM_EMAIL = 'postmaster@sandbox34d90c59e46f47fea6769287f3b64536.mailgun.org'
    FROM_TITLE = "Stores Rest API"
    
    

    @classmethod
    def send_email(
        #The email is a list of strings because we might want to send email to several users and again because we are going to import the class
        cls, email: List[str], subject: str, text: str, html: str
    ) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(gettext("mailgun_failed_load_api_key"))

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(gettext("mailgun_failed_load_domain"))

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                #the above imported constant has cls because it is coming from that class
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailGunException(gettext("mailgun_error_send_email"))

        return response
