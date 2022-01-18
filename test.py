import collections
from email.message import EmailMessage
from flask import request
from flask.helpers import  url_for
from libs.mailgun import  GoogleMail
from requests import Response

def resend_confirmation_email(username, email, ids) -> Response:

    #link = request.url_root[:-1] + url_for("confirmation", confirmation_id=ids)  #change this from the user_id to confirmation_id in other to secure the id of the user #the link for user to click
    link = 'http://localhost'
    subject = "Email Confirmation"
    text = f"Please click the link to confirm your registration: {link}"
    html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
    GoogleMail.send_mail(username, email, text)
    
username = 'phoenix'
email = 'nathking75@yahoo.com'
ids = '5'
resend_confirmation_email(username, email, ids)