import yaml
import os

ROOT_PATH = os.path.dirname(__file__)

CONFIG_FILE_PATH = os.path.join(ROOT_PATH, 'env.yaml')

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as r_file:
        data = yaml.safe_load(r_file) or dict()
else:
    data = dict()

DATA_ENCRYPTION_KEY = data.get('DATA_ENCRYPTION_KEY', '')
