import ProjectConfigs
import smtplib

def login() -> smtplib.SMTP:
    """
    Executes steps for connecting to SMTP server and logging in
    :return: smtplib.SMTP object to use for sending emails
    """
    smtp = smtplib.SMTP(ProjectConfigs.configs['emailConfigs']['smtpHost'], ProjectConfigs.configs['emailConfigs']['smtpPort'])
    smtp.ehlo()
    smtp.starttls()
    smtp.login(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['password'])
    return smtp

def test_login() -> None:
    """
    Executes steps for connecting to SMTP server and logging in, and immediately quits connection afterward.
    Intended to be used at the start of run time, to check if provided credentials are valid before using them in the rest of the program.
    """
    smtp = login()
    smtp.quit()

def send_email(smtp: smtplib.SMTP, msg_body: str) -> None:
    """
    Sends price drop email
    :param smtp: smtplib.SMTP object handling the send
    :param msg_body: Email body for the email containing price drop information
    """
    subject = "A price drop was detected!"
    # TODO: change link to hyperlink and add link to source code
    signature = "Sent from Python\nDeveloped by Tristan Samonte\nhttps://www.linkedin.com/in/tsamonte23/"
    msg_whole = f"Subject: {subject}\n{msg_body}\n{signature}"
    smtp.sendmail(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['receiverEmail'], msg_whole)
