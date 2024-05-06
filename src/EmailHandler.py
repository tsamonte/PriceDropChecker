import ProjectConfigs
import smtplib
from email.mime.text import MIMEText

def login() -> smtplib.SMTP:
    smtp = smtplib.SMTP(ProjectConfigs.configs['emailConfigs']['smtpHost'], ProjectConfigs.configs['emailConfigs']['smtpPort'])
    smtp.ehlo()
    smtp.starttls()
    smtp.login(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['password'])
    return smtp
def test_login():
    smtp = login()
    smtp.quit()

def send_email(smtp: smtplib.SMTP, msg_body: str):
    # subject = "A price drop was detected!"
    subject = "Test email for Price Checker"
    # TODO: change link to hyperlink
    signature = "Sent from Python\nDeveloped by Tristan Samonte\nhttps://www.linkedin.com/in/tsamonte23/"
    msg_whole = f"Subject: {subject}\n{msg_body}\n\n{signature}"
    smtp.sendmail(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['receiverEmail'], msg_whole)

class EmailHandler:

    def __init__(self):
        try:
            # TODO: Can handle exceptions at instantiation. All smtplib errors inherit from smtplib.SMTPException
            self.smtp = smtplib.SMTP(ProjectConfigs.configs['emailConfigs']['smtpHost'], ProjectConfigs.configs['emailConfigs']['smtpPort'])
            code, _ = self.smtp.ehlo() # 250 if success
            if code != 250:
                raise smtplib.SMTPException("ehlo call was unsuccessful")
            self.smtp.starttls()
            self.smtp.login(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['password'])
        except Exception as e:
            print("There was an error trying to connect to the SMTP server:\n{e}")
            raise

    # def reconnect(self):
    #     self.smtp.starttls()
    #     self.smtp.login(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['password'])

    def send_email(self, msg_body: str):
        subject = "A price drop was detected!"
        signature = "Sent from Python\nDeveloped by Tristan Samonte\na | a"
        msg_whole = f"Subject: {subject}\n{msg_body}\n\n{signature}"
        self.smtp.sendmail(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['receiverEmail'], msg_whole)
