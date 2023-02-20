import os
import pythoncom
import win32com.client


class Autostart:
    """A class to manage autostart of a program on Windows."""

    def __init__(self, Env):
        """
        Initialize the Autostart class.

        Parameters:
        Env: object
            An instance of the `Env` class that provides access
            to environment variables.

        Returns:
        None
        """
        print("Autostart")
        self.my_env = Env
        self.STARTUP_PATH = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"

    def add_to_shell_startup(self):
        """
        Add the program to the Windows shell:startup so it starts automatically.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        pth = os.getcwd()
        s_name = "main.exe"
        shortcut_name = "main.lnk"
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(
            os.path.join(self.STARTUP_PATH, shortcut_name)
        )
        shortcut.Targetpath = f"{pth}\\{s_name}"
        shortcut.WorkingDirectory = pth
        shortcut.save()

    def ask_for_autostart_setup(self, choice, agree_to_email=0):
        """
        Ask the user if they want to add the program to the autostart,
        and if so, add it.

        Parameters:
        choice: str
            A string indicating the user's choice ("1" to add the program
            to autostart, "0" otherwise).
        agree_to_email: int, optional
            Should not be changed. It has no effect.
            An integer indicating whether the user has agreed to send
            email logs (0 for "no", 1 for "yes").

        Returns:
        --------
        bool
            True if the user has made a choice, False otherwise.
        """
        key = "AUTOSTART"
        if choice == "1":
            self.add_to_shell_startup()
        self.my_env.configure_env_var(key=key, value=choice)
        return True
