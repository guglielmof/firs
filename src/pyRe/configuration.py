from .utils import singleton
import configparser
import os

@singleton
class configuration:

    def __init__(self, config_path=None):
        self.set_config(config_path)

    def get_configs(self):
        return self.config

    def set_config(self, config_path=None):
        if config_path is None:
            config_path = os.path.dirname(os.path.abspath(__file__)) + "/configs/default_config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
