import re
import os
from contact.trusted_person import Person
from env.configure_env import Env_Configure
from autostart.autostart import Autostart
from error.errors import error_handler


class Menu:
    def __init__(self) -> None:
        self.my_env = Env_Configure()
        self.autostart = Autostart(self.my_env)
        self.welcome_message = (
            "Welcome WatrchfulEye script.\n"
            "\nIts idea is to log your keystrokes.\n"
            "If it happens that you will type any words, name or websites which can be"
            "considered as threat.\n"
            "It will log this event and pass this info either "
            "to yourself or your TRUSTED PERSON.\n"
            "\nIMPORTANT NOTICE:\n"
            "This program works as keylogger.\n"
            "So if you decide to connect this script to send mails to someone make sure that\n"
            "THIS PERSON IS TRUSTED.\n"
            "\nIn following steps you will go through basic setup.\n"
            " "
        )
        self.menu_flag = True
        if os.environ["SECRUITY_CODE"] == "default":
            self.was_configured = False
        else:
            self.was_configured = True

    def save_in_dotenv(self, credentials):
        self.my_env.configure_env_var(key=credentials[0], value=credentials[1])

    def will_to_send_emails(self, choice, agree_to_email=0):
        permission_to_send_tuple = ("PERMISSION_TO_SEND", choice)
        self.save_in_dotenv(permission_to_send_tuple)
        return True

    def check_email(self, email):
        regex = r"\b[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}\b"
        if re.match(regex, email) is None:
            return False
        return True

    def define_trusted_contact(self, choice, agree_to_email="0"):
        if agree_to_email == "0":
            trusted_contact_tuple = ("TRUSTED_CONTACT", choice)
            self.save_in_dotenv(trusted_contact_tuple)
            return True
        elif agree_to_email == "1":
            if self.check_email(choice):
                trusted_contact_tuple = ("TRUSTED_CONTACT", choice)
                self.save_in_dotenv(trusted_contact_tuple)
                return True
            error_handler("Trusted contact")
        return False

    def senders_email(self, choice, agree_to_email="0"):
        if agree_to_email == "0":
            trusted_contact_tuple = ("SENDERS_EMAIL", choice)
            self.save_in_dotenv(trusted_contact_tuple)
            return True
        elif agree_to_email == "1":
            if self.check_email(choice):
                senders_email_tuple = ("SENDERS_EMAIL", choice)
                self.save_in_dotenv(senders_email_tuple)
                return True
            error_handler("Senders email")
        return False

    def senders_password(self, password, agree_to_email="0"):
        if agree_to_email == "0":
            trusted_contact_tuple = ("SENDERS_PASSWORD", password)
            self.save_in_dotenv(trusted_contact_tuple)
            return True
        elif agree_to_email == "1":
            if len(password) != 16:
                error_handler("Too short password")
                return False
            trusted_contact_tuple = ("SENDERS_PASSWORD", password)
            self.save_in_dotenv(trusted_contact_tuple)
            return True

    def line_length(self, choice, agree_to_email="0"):
        key = "LINE_LENGTH"
        try:
            try_to_int = int(choice)
            self.my_env.configure_env_var(key=key, value=choice)
            return True
        except:
            error_handler("Length needs to be a number")
            return False

    @staticmethod
    def send_email_with_secruity_code():
        person = Person()
        code = person.create_secruity_code()
        person.save_secruity_code(code)
        person.email_with_secruity_code()

    def check_secruity_code(self):
        self.secruity_code = os.environ["SECRUITY_CODE"]
        if self.secruity_code == "default":
            return True
        password = input()
        while True:
            if password.lower() == "exit":
                return False
            if password == self.secruity_code:
                return True
            if password != self.secruity_code:
                password = input("Wrong secruity_code. Please try again:\n")

    def finish(self):
        self.menu_flag = False
        return True
