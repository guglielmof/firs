from .utils import singleton
import configparser
import os
import warnings

@singleton
class configuration:


    def get_config(self):
        try:
            return self.config
        except AttributeError:
             raise AttributeError("configuration not available: have you run firs.configure(<config path>) first?")

    def set_config(self, config_path=None):

        if config_path is None:
            raise ValueError("configuration path not specified")

        if not os.path.exists(config_path):
            raise ValueError(f"configuration file not found. Path {config_path} migth be unvalid.")

        self.config = configparser.ConfigParser()
        self.config.read(config_path)


        if 'paths' not in self.config.sections():
            warnings.warn("key sections are missing from the config file: are you sure you specified the rigth path?")
