# key = paltghsckxotraim
import smtplib
import ssl
def send(Recipient,):
    password=None
    from email.message import EmailMessage
    with open("password.txt",'r') as f:
        password=f.readline()
    email_sender = 'guzamo60@gmail.com'
    email_password = password
    email_receiver = Recipient
     
    subject='Medical records'
    body=