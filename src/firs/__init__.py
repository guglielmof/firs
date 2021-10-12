import configparser
import sys

from .configuration import configuration

from .simple_test import simple_test

from .trecdata import *

from .replicator import *

import os


def configure(config_path):
	configuration().set_config(config_path)


def get_configurations():

	return configuration().get_config()