import os
from pathlib import Path
import json
from email_process.emails import SendEmail
import datetime
from email.mime.base import MIMEBase


class Logs:
    def __init__(self) -> None:
        self.path = Path.cwd() / "logs_process" / "logs"
        self.files_list = self.get_logs_from_dir()
        self.current_log = self.determine_current_log()
        self.past_logs = self.get_past_logs()
        self.email_subject = f"WatchfulEye - Suspicious Activity Spotted"
        self.email_message_content = (
            f"It is possible that an user of this software who chosen you as a safe person has done some supicious acitivy. In attachment you can find his current log.\n"
            f"Just open it to find out more."
        )
        self.create_new_email()
        self.email_has_attachment = False
        self.current_log_lines = self.check_lines_in_logs(self.current_log)

    def get_logs_from_dir(self) -> list:  # Works
        files = os.listdir(self.path)
        files_list = [
            file
            for file in files
            if os.path.isfile(os.path.join(self.path, file))
        ]
        return files_list

    def create_new_email(self):
        self.email_message = SendEmail(
            self.email_subject, self.email_message_content
        )

    def determine_current_log(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        for file in self.files_list:
            if timestamp in file:
                return file

    def get_past_logs(self) -> list:
        logs_list_without_current_log = self.files_list[:]
        logs_list_without_current_log.remove(self.current_log)
        return logs_list_without_current_log

    def check_lines_in_logs(self, log_file) -> int:
        with open(os.path.join(self.path, log_file), "r") as log_f:
            lines = log_f.readlines()
            return len(lines)

    def check_logs_in_history(self, log_list):
        path = Path(__file__).parent / "logs_history.json"
        with open(path, "r", encoding="utf-8") as f:
            try:
                sent_logs = json.load(f)

                for log in sent_logs:
                    if log in log_list:
                        log_list.remove(log)
            except:
                pass

    def check_history_logs_content(self, logs_list):
        self.check_logs_in_history(log_list=logs_list)
        for log in logs_list:
            self.check_log_length(log)

    def attach_log(self, log):
        log_path = os.path.join(self.path, log)
        self.email_message.create_attachment(attach_path=log_path)
        self.email_has_attachment = True

    def add_send_log_to_json(self, log_file, is_empty):
        path = Path(__file__).parent / "logs_history.json"
        with open(path, "r", encoding="utf-8") as file:
            try:
                sent_logs_history = json.load(file)
            except json.decoder.JSONDecodeError:
                sent_logs_history = {}

        sent_logs_history[log_file] = is_empty
        with open(path, "w", encoding="utf-8") as file:
            json.dump(sent_logs_history, file)

    def check_log_length(self, log):
        if self.check_lines_in_logs(log) > 0:
            self.attach_log(log=log)
            if not log == self.current_log:
                self.add_send_log_to_json(log, True)
        if self.check_lines_in_logs(log) == 0:
            if not log == self.current_log:
                self.add_send_log_to_json(log, False)

    def update_current_log_lines(self):
        self.current_log_lines = self.check_lines_in_logs(self.current_log)

    def current_log_attaching(self):
        updated_lines_in_current_log = self.check_lines_in_logs(
            self.current_log
        )
        if updated_lines_in_current_log > self.current_log_lines:
            self.attach_log(self.current_log)
            self.current_log_lines = updated_lines_in_current_log

    def send_email_with_logs(self):
        if self.email_has_attachment == True:
            self.email_message.create_smtp_session()
            print("Email sent")
            self.email_has_attachment = False
        else:
            pass
