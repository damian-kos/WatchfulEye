import keyboard
from pathlib import Path
import multiprocessing
import logging
import datetime
import os
import schedule
from logs_process.logs_processing import Logs
import time
from menu.gui import Gui


timestamp = datetime.datetime.now().strftime("%Y%m%d")
log_dir = Path(__file__).parent / "logs_process/logs"
log_file = f"log_{timestamp}.log"
log_path = os.path.join(log_dir, log_file)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=log_path,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    encoding="utf-8",
)


def producer(que_data):
    """
    This function starts recording the key presses using the
    keyboard library and waits for the user to press either
    'space' or 'enter' key.
    When either key is pressed, it calls the 'filter_and_queue_data' function which
    process the recorded data, filters it and adds the filtered data
    to the 'que_data' queue.

    Parameters:
    que_data (Queue): A queue to which the filtered data will be added.

    Returns:
    None
    """

    keyboard.add_hotkey(
        "space", lambda: filter_and_queue_data(recorded_key_press)
    )
    keyboard.add_hotkey(
        "enter", lambda: filter_and_queue_data(recorded_key_press)
    )

    # Start recording key presses
    recorded_key_press = keyboard.start_recording()

    def filter_and_queue_data(recorded):
        """
        This function processes the recorded data, filters it, and adds
        the filtered data to the 'que_data' queue if the length is
        greater than 29.

        Parameters:
        recorded: The recorded key presses.

        Returns:
        None
        """
        joined_words = ""
        # Convert the recorded data to a strings list.
        typed_words = list(keyboard.get_typed_strings(recorded[0].queue))
        # This removes unexpected empty spaces and makes it more
        # readable.
        joined_words = " ".join(typed_words).split()
        joined_words = " ".join(joined_words)
        if len(joined_words) > 29:
            que_data.put(joined_words)
            recorded_key_press[0].queue.clear()

    keyboard.wait()


def consumer(que_data):
    """
    This function consumes data from the 'que_data' queue and checks if
    any of the data contains any threat words.
    The threat words are read from a file called 'threats.txt' and are
    stored in a list called 'lines'.
    If a threat word is found, the function logs a warning message
    containing the data that contains the threat word.

    Parameters:
    que_data (Queue): A queue containing data that needs to be checked for threat words.

    Returns:
    None
    """
    print("consumer working...")
    threat_path = Path(__file__).parent / "threats.txt"
    with open(threat_path, encoding="utf-8") as file:
        threat_words = file.readlines()
    while True:
        sentence_to_check = que_data.get()
        for word in threat_words:
            if (
                word.replace("\n", "").replace(" ", "").lower()
                in sentence_to_check.replace(" ", "").lower()
            ):
                logging.warning(f"{sentence_to_check}:  {word}")


def scheduled_emails():
    """
    This function is responsible for scheduling and sending emails
    containing logs.
    It creates an instance of the 'Logs' class, calls its
    'check_history_logs_content' method to check the contents of
    the past logs,
    and then calls its 'send_email_with_logs' method to send the email.
    It also defines a 'send_email' function, which creates a new email,
    attaches the current log to it and sends it.
    The function then uses the schedule library to schedule
    the 'send_email' function to run every hour.
    It enters an infinite loop to keep checking for any scheduled task
    and runs them accordingly.

    Parameters:
    None

    Returns:
    None
    """
    logs = Logs()
    logs.check_history_logs_content(logs.past_logs)

    logs.send_email_with_logs()

    def send_email():
        """This function creates a new email, attaches the current log to
        it, and sends the email using the 'Logs' class instance.

        Parameters:
            None

        Returns:
            None"""
        logs.create_new_email()
        logs.current_log_attaching()
        logs.send_email_with_logs()

    schedule.every().hour.do(send_email)

    while True:
        schedule.run_pending()
        time.sleep(10)


def gui_process():
    """
    Creates an instance of the 'Gui' class and runs the
    GUI.

    Parameters:
    None

    Returns:
    None
    """
    gui = Gui()
    gui.run_gui()


if __name__ == "__main__":
    """
    This is the main block of code that starts the multiprocessing
    processes, creates the 'que_data' queue and initializes the GUI.
    It waits for the GUI to finish and then starts the other processes.
    It also waits for the other processes to finish before exiting.
    """
    multiprocessing.freeze_support()

    que_data = multiprocessing.Queue()
    p0 = multiprocessing.Process(target=gui_process)
    p0.start()
    p0.join()

    p1 = multiprocessing.Process(target=producer, args=(que_data,))
    p2 = multiprocessing.Process(target=consumer, args=(que_data,))
    p3 = multiprocessing.Process(target=scheduled_emails)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
