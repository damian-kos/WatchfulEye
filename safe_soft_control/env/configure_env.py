import dotenv
import os


class Env_Configure:
    def __init__(self) -> None:
        """
        Initializes the Env_Configure class and loads the .env file.

        Returns:
            None
        """
        self.dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(self.dotenv_file)

    def configure_env_var(self, key, value=None):
        """Configures environment variables.

        Args:
            key (str): Name of environment variable.
            value (str, optional): Value of environment variable.
            Defaults to None.
        """
        os.environ[key] = value
        dotenv.set_key(self.dotenv_file, key, os.environ[f"{key}"])
