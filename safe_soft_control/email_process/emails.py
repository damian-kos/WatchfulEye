import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from env.configure_env import Env_Configure
import os


class SendEmail:
    """A class for creating and sending emails.

    Attributes:
        mail_content (str): The content of the email message.
        my_env (Env_Configure): The environment variable manager.
        sender_address (str): The email address of the sender.
        sender_pass (str): The password for the sender's email account.
        receiver_address (str): The email address of the receiver.
        message (MIMEMultipart): The message object that represents the email.

    """

    def __init__(self, subject, message) -> None:
        """Initializes the SendEmail object.

        Args:
            subject (str): The subject of the email.
            message (str): The content of the email message.
        """
        self.mail_content = message
        self.my_env = Env_Configure()
        # The mail addresses and password
        self.sender_address = os.environ["SENDERS_EMAIL"]
        self.sender_pass = os.environ["SENDERS_PASSWORD"]
        self.receiver_address = os.environ["TRUSTED_CONTACT"]

        # Setup the MIME
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_address
        self.message["To"] = self.receiver_address
        self.message["Subject"] = subject  # The subject line
        self.message.attach(MIMEText(self.mail_content))

    def create_attachment(self, attach_path):
        """Creates an attachment and adds it to the email.

        Args:
            attach_path (str): The path to the file to attach.

        """
        attachmentPath = attach_path
        try:
            with open(attachmentPath, "rb") as attachment:
                p = MIMEApplication(attachment.read(), _subtype="log")
                p.add_header(
                    "Content-Disposition",
                    "attachment; filename= %s" % attachmentPath.split("\\")[-1],
                )
                self.message.attach(p)
        except Exception as e:
            pass

    def create_smtp_session(self):
        """Creates an SMTP session and sends the email."""
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(
            self.sender_address, self.sender_pass
        )  # login with mail_id and password
        text = self.message.as_string()
        session.sendmail(self.sender_address, self.receiver_address, text)
        session.quit()
