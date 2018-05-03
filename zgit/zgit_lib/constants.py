import os

class Constants(object):
	zgit_dir = os.path.abspath(os.path.expanduser("~/.zgit"))
	default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "default_config.json")