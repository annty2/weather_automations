from configparser import ConfigParser
import os

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')

config = ConfigParser()

config.read(config_path)

API_KEY = config['API']['API_KEY']
BASE_URL = config['API']['BASE_URL']
DB_NAME = config['DB']['DB_NAME']



