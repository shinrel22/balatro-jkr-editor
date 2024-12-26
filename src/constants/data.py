import json
import os

from src.utils import decompress_data
from src.constants.dirs import DATA_DIR, TMP_DIR
from config import DATA_ENCRYPTION_KEY


def load_data_from_file(data_path: str, tmp_path: str) -> dict:
    data = None
    if os.path.exists(tmp_path):
        data = json.load(open(tmp_path))

    if not data:
        data = decompress_data(
            data=open(data_path, 'rb').read(),
            encryption_key=DATA_ENCRYPTION_KEY
        )
        data = json.loads(data.decode())

        with open(
                tmp_path,
                'w'
        ) as fr:
            fr.write(json.dumps(data))

    return data


PARSED_DATA_DIR = os.path.join(TMP_DIR, 'data')
if not os.path.exists(PARSED_DATA_DIR):
    os.makedirs(PARSED_DATA_DIR)

TAGS = load_data_from_file(
    data_path=os.path.join(DATA_DIR, 'tags.dat'),
    tmp_path=os.path.join(PARSED_DATA_DIR, 'tags.json'),
)

JOKERS = load_data_from_file(
    data_path=os.path.join(DATA_DIR, 'jokers.dat'),
    tmp_path=os.path.join(PARSED_DATA_DIR, 'jokers.json'),
)
