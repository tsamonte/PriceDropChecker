import ProjectConfigs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    # Initialize MIME object message container
    msg_whole = MIMEMultipart()
    msg_whole["From"] = ProjectConfigs.configs['emailConfigs']['senderEmail']
    msg_whole["To"] = ProjectConfigs.configs['emailConfigs']['receiverEmail']
    msg_whole["Subject"] = "A price drop was detected!"

    # Initialize email signature string
    signature = """\
    <html>
        <body>
            <p>
                Sent from Python
                <br>Developed by Tristan Samonte (<a href="https://github.com/tsamonte/PriceDropChecker">Source</a>)
                <br><a href="https://www.linkedin.com/in/tsamonte23">LinkedIn</a> | <a href="https://github.com/tsamonte">GitHub</a>
            </p>
        </body>
    </html>
    """

    # Add the message body and signature to message container
    msg_whole.attach(MIMEText(msg_body, 'html'))
    msg_whole.attach(MIMEText(signature, 'html'))

    # Send the email
    smtp.sendmail(ProjectConfigs.configs['emailConfigs']['senderEmail'],
                  ProjectConfigs.configs['emailConfigs']['receiverEmail'], msg_whole.as_string())
