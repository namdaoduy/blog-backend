import os.path
from importlib import import_module

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv('ENVIRONMENT', 'local')
if env not in ['local', 'test']:
    config_file = 'main/cfg/' + env + '.py'
    if not os.path.isfile(config_file):
        env = 'local'

config_name = 'main.cfg.' + env

module = import_module(config_name)

config = module.config
