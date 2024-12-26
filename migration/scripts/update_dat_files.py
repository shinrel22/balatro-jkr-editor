import os.path

from src.constants.dirs import DATA_DIR, TMP_DIR
from src.utils import compress_data
from config import DATA_ENCRYPTION_KEY

file_names = [
    'tags',
    'tarots',
    'jokers',
    'planets',
    'spectrals',
]

for file_name in file_names:
    dat_path = os.path.join(DATA_DIR, f'{file_name}.dat')
    json_path = os.path.join(TMP_DIR, f'data/{file_name}.json')

    with open(dat_path, 'wb') as fr:
        fr.write(compress_data(
            data=open(json_path, 'rb').read(),
            encryption_key=DATA_ENCRYPTION_KEY
        ))
