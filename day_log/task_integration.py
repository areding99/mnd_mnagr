import sys

sys.path.append('../task_management')

from lib.config_parser import ConfigParser

cp = ConfigParser()
config = cp.get_config()
