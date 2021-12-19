import smtplib
from email.message import EmailMessage

class EmailHandler(object):
    def __init__(self):
        pass
    
    def send_email(self, recipient, content, subject="Trading Client Mail!"):
        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = "TradingClient@HolleranInd.com"
        msg["To"] = recipient

        #TODO: https://serverfault.com/questions/833809/send-mail-without-mta-gmail-etc
        with smtplib.SMTP_SSL("smtp.google.com", 465) as s:
            s.send_message(msg)
