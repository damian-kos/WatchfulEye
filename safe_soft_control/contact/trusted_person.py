import secrets
import os
from email_process.emails import SendEmail
from env.configure_env import Env_Configure


class Person:
    """
    A class that represents a person and provides methods to manage security codes.

    Attributes:
        my_env (Env_Configure): An instance of the Env_Configure class for environment variable configuration.
    """

    def __init__(self):
        """
        Initializes a new instance of the Person class with a new instance of Env_Configure.
        """
        self.my_env = Env_Configure()

    def create_secruity_code(self):
        """
        Generates a random 8-digit security code using the secrets module.

        Returns:
            The generated security code as a string.
        """
        secruity_code = secrets.token_hex(8)
        return secruity_code

    def save_secruity_code(self, code):
        """
        Saves a security code to an environment variable.

        Args:
            code: The security code to be saved as a string.
        """
        key = "SECRUITY_CODE"
        self.my_env.configure_env_var(key=key, value=code)

    def email_with_secruity_code(self):
        """
        Sends an email with the current security code to the user.
        """
        email_subject = f"Safe Soft Control"
        email_message_code = (
            f"Here is your SECRUITY_CODE: {os.environ['SECRUITY_CODE']}"
        )
        create_message_with_secruity_code = SendEmail(
            email_subject, email_message_code
        )
        create_message_with_secruity_code.create_smtp_session()
