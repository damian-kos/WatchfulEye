import dearpygui.dearpygui as dpg
from .initial_run import Menu
import os
from env.configure_env import Env_Configure



class Gui:
    def __init__(self) -> None:
        self.remaining = 10
        self.time = 1
        dpg.create_context()
        dpg.create_viewport(title="Custom Title", width=800, height=600)
        self.menu = Menu()
        self.my_env = Env_Configure()
        self.password = os.environ["SECRUITY_CODE"]
        self.options = {
            "1. Do you want to send emails to Trusted Person?": "will_to_send_emails",
            "2. Type Trusted Person's contact email": "define_trusted_contact",
            "3. Type your's email": "senders_email",
            "4. Type your's password": "senders_password",
            "5. Do you want to run this app everytime your machine starts up?": "autostart.ask_for_autostart_setup",
        }
        self.welcome_message = (
            "Welcome to Safe Soft Control script.\n"
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

    def menu_text(self):
        for count, (choice, option) in enumerate(self.options.items()):
            dpg.add_text(choice)
            if count == 0 or count == 4:
                dpg.add_checkbox(callback=self.checkbox_callback, tag=option)
            elif count == 1 or count == 2:
                dpg.add_input_text(tag=option, enabled=False)
            elif count == 3:
                dpg.add_input_text(tag=option, enabled=False)
        dpg.add_button(label="Save", tag="finish", callback=self.save_button_callback)

    def checkbox_callback(self):
        # Disable text input windows since user didn't want mails to be send.
        if dpg.get_value("will_to_send_emails") == False:
            for item in list(self.options.values())[1:4]:
                dpg.configure_item(item, enabled=False, default_value="")
        # Enables them back if user changes his mind.
        if dpg.get_value("will_to_send_emails") == True:
            for item in list(self.options.values())[1:4]:
                dpg.configure_item(item, enabled=True)

    def save_button_callback(self):
        self.user_choice = []
        for item in list(self.options.values())[:5]:
            if dpg.get_value(item) == True:
                self.user_choice.append("1")
            elif dpg.get_value(item) == False:
                self.user_choice.append("0")
            elif dpg.get_value == "":
                self.user_choice.append(" ")
            else:
                self.user_choice.append(dpg.get_value(item))
        if self.configure_app_after_save():
            self.window_after_save()


    def configure_app_after_save(self):
        func_options = [
            self.menu.will_to_send_emails,
            self.menu.define_trusted_contact,
            self.menu.senders_email,
            self.menu.senders_password,
            self.menu.autostart.ask_for_autostart_setup,
        ]
        if int(self.user_choice[0]) == 0:
            for choice, setting in zip(self.user_choice, func_options):
                setting(choice, agree_to_email=int(self.user_choice[0]))
            return True
        else:
            for choice, setting in zip(self.user_choice, func_options):
                if not setting(choice, agree_to_email=1):
                    name = setting.__func__.__name__
                    # print(f"ERROR {setting.__func__.__name__}")
                    with dpg.window(modal=True, label="error") as error:
                        dpg.add_text(f"{name}")
                        dpg.add_button(label="OK", user_data=(name), width=100, callback=lambda: dpg.delete_item(error))
                    return False
            return True
   

    def app_set(self):
        self.set = os.environ["IS_SETUP"]
        if self.set == "1":
            return True
        return False


    def window_after_save(self):
        confirmed_info = [
            "Agreed to send emails: ",
            "Your Trusted Person: ",
            "Email you will send messages from: ",
            "Password: ",
            "You allowed app to start with every machine startup: ",
        ]
        with dpg.window(tag="saved_window", label="Saved sucessfully!"):
            for info, item in zip(confirmed_info, self.user_choice):
                if item == "1":
                    item = "Yes"
                elif item == "0":
                    item = "No"
                dpg.add_text(f"{info}{item}")
            dpg.add_button(
                label="Ok", callback=self.delete_after_save_and_lock_with_password
            )

    def delete_after_save_and_lock_with_password(self):
        dpg.delete_item("saved_window")
        self.password = os.environ["SECRUITY_CODE"]
        self.app_already_setup()

    def create_menu_window(self):
        with dpg.window(tag="tutorial_window", label="Tutorial"):
            if not self.app_set():
                self.welcome_message = (
                    f"Hello, this is your first setup\n\n{self.welcome_message}"
                )
            else:
                self.app_already_setup()
            dpg.add_text(self.welcome_message)
            self.menu_text()

    def check_password(self):
        if dpg.get_value("password") == self.password:
            dpg.delete_item("password_window")

    def exit_gui(self):
        if not self.app_set():
            self.my_env.configure_env_var(key="IS_SETUP", value="1")
        dpg.stop_dearpygui()

    def app_already_setup(self):
        with dpg.window(
            tag="password_window",
            label="Password",
            width=500,
            pos=(200, 100),
            modal=True,
            no_close=True,
        ):
            if self.password == "default":    
                dpg.add_text("You setup your app and now can run a script, or\n"
                    "You can change it's settings.\n"
                    "NOTE: Later on this script will run automatically after 20 seconds.")            
                dpg.add_button(
                    label="Change Settings", tag="enter_settings", callback=lambda: dpg.delete_item("password_window")
                )            
                dpg.add_button(label="Run Script", tag="script_run", callback=self.exit_gui)
            else:
                dpg.add_text(
                "Looks like you already configured this app.\n"
                "Script will run automatically in 20 seconds.\n"
                " "
                )
                dpg.add_text("To access settings: \n"
                    "Please type in a password which was sent to your Trusted Person.\n"
                    " ")
                dpg.add_input_text(tag="password")
                dpg.add_button(
                    label="Log in", tag="enter_password", callback=self.check_password
                )
                dpg.add_button(label="Run Script", tag="script_run", callback=self.exit_gui)
    
    # def countdown(self):
    #     print(dpg.get_total_time())

    def run_gui(self):
        # with dpg.handler_registry(tag="widget_handler") as handler:
        #     dpg.add_item_visible_handler(callback=self.countdown)

        # dpg.bind_item_handler_registry("script_run", "widget_handler")
        dpg.setup_dearpygui()
        self.create_menu_window()
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            if self.app_set() and dpg.does_item_exist("script_run"):
                time = int(dpg.get_total_time()) % 10
                dpg.configure_item("script_run", label=f"Run Script ({20 - int(time)})")
                if 20-int(time) == 0:
                    dpg.stop_dearpygui()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

