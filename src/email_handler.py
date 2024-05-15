import ProjectConfigs
import smtplib
import email.errors
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from CustomLogger import logger

def login() -> smtplib.SMTP:
    """
    Executes steps for connecting to SMTP server and logging in
    :return: smtplib.SMTP object to use for sending emails
    """
    try:
        logger.info(f"Attempting login at {ProjectConfigs.configs['emailConfigs']['smtpHost']}:{ProjectConfigs.configs['emailConfigs']['smtpPort']}")
        smtp = smtplib.SMTP(ProjectConfigs.configs['emailConfigs']['smtpHost'], ProjectConfigs.configs['emailConfigs']['smtpPort'])
        smtp.ehlo()
        smtp.starttls()
        smtp.login(ProjectConfigs.configs['emailConfigs']['senderEmail'], ProjectConfigs.configs['emailConfigs']['password'])
        return smtp
    # Catch and rethrow.
    # If exception happens at initialization (within email_handler.test_login()), end program
    # If exception happens during the core app logic (within price_check.notify_price_drops()), don't end program
    except (smtplib.SMTPException, smtplib.SMTPResponseException) as smtp_exc:
        logger.error(f"There was an issue trying to connect to the email server:\n\t{smtp_exc}")
        raise
    except Exception as e:
        logger.error(f"There was an issue during login:\n{e}")
        raise

def test_login() -> None:
    """
    Executes steps for connecting to SMTP server and logging in, and immediately quits connection afterward.
    Intended to be used at the start of run time, to check if provided credentials are valid before using them in the rest of the program.
    """
    # Since this is called during project initialization to validate login, an exception should end program
    smtp = login()
    smtp.quit()

def send_email(smtp: smtplib.SMTP, msg_body: str) -> None:
    """
    Sends price drop email
    :param smtp: smtplib.SMTP object handling the send
    :param msg_body: Email body for the email containing price drop information
    """
    try:
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

    except email.errors.MessageError as me:
        logger.error(f"An error occurred while building the email notification:\n\t{me}")
    except (smtplib.SMTPException, smtplib.SMTPResponseException) as smtp_exc:
        logger.error(f"There was an issue trying to send the email notification:\n\t{smtp_exc}")
    except Exception as e:
        logger.error(f"There was an issue trying to build/send the email:\n\t{e}")
