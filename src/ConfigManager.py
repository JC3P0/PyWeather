import os
import platform
import configparser
import logging

# Configure logging to display information messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    CONFIG_FILE_PATH = ""

    @staticmethod
    def get_config_file_path():
        """
        Determine the appropriate path for the configuration file based on the operating system.
        """
        if ConfigManager.CONFIG_FILE_PATH:
            return ConfigManager.CONFIG_FILE_PATH

        # Identify the operating system
        os_name = platform.system().lower()

        # Set the config file path based on the operating system
        if 'windows' in os_name:
            ConfigManager.CONFIG_FILE_PATH = os.path.join(os.getcwd(), 'config.ini')
        elif 'darwin' in os_name:  # macOS
            ConfigManager.CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'PyWeather', 'config.ini')
        elif 'linux' in os_name or 'nix' in os_name or 'aix' in os_name:
            ConfigManager.CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.config', 'PyWeather', 'config.ini')
        else:
            raise Exception(f"Unsupported operating system: {os_name}")

        # Log the path to the config file
        logger.info(f"Config file path: {ConfigManager.CONFIG_FILE_PATH}")
        return ConfigManager.CONFIG_FILE_PATH

    @staticmethod
    def save_config(config):
        """
        Save the configuration to the file. Create the directory if it does not exist.
        """
        # Get the directory of the config file
        config_dir = os.path.dirname(ConfigManager.get_config_file_path())
        
        # Create the directory if it doesn't exist
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logger.info(f"Config directory created at {config_dir}")

        # Write the configuration to the file
        with open(ConfigManager.CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def load_config():
        """
        Load the configuration from the file. Return an empty config if the file does not exist.
        """
        config = configparser.ConfigParser()

        # Check if the config file exists and read it
        if os.path.exists(ConfigManager.get_config_file_path()):
            config.read(ConfigManager.get_config_file_path())
        else:
            logger.info("Config file does not exist.")
        
        return config

    @staticmethod
    def ensure_config_exists():
        """
        Ensure the configuration file exists and has the required sections.
        Create a default configuration if necessary.
        """
        config = ConfigManager.load_config()

        # Check if the 'Settings' section exists, add it if not
        if not config.has_section('Settings'):
            config.add_section('Settings')
            ConfigManager.save_config(config)
            logger.info("Config file created with 'Settings' section")

        # Check if the API key is present in the config
        if not config.get('Settings', 'api_key', fallback=None):
            logger.info("API key is missing or empty in config")
            return False  # Indicate that the API key is missing

        return True  # Indicate that the API key is present

    @staticmethod
    def save_api_key(api_key):
        """
        Save the API key to the configuration file.
        """
        config = ConfigManager.load_config()

        # Add the 'Settings' section if it does not exist
        if not config.has_section('Settings'):
            config.add_section('Settings')

        # Set the API key in the config
        config.set('Settings', 'api_key', api_key)
        ConfigManager.save_config(config)

    @staticmethod
    def delete_api_key():
        """
        Remove the API key from the configuration file.
        """
        config = ConfigManager.load_config()

        # Check if the API key exists in the config and remove it
        if config.has_section('Settings') and config.has_option('Settings', 'api_key'):
            config.remove_option('Settings', 'api_key')
            ConfigManager.save_config(config)
            logger.info("Invalid API key removed from config")
