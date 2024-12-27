import json
import os.path

from src.constants.dirs import DATA_DIR, TMP_DIR
from src.utils import compress_data
from src import JkrEditor
from config import DATA_ENCRYPTION_KEY


file_name = 'jokers'
dat_path = os.path.join(DATA_DIR, f'{file_name}.dat')
json_path = os.path.join(TMP_DIR, f'data/{file_name}.json')

jkr_file_path = '/home/shin/.local/share/Steam/steamapps/compatdata/2379780/pfx/drive_c/users/steamuser/AppData/Roaming/Balatro/1/save.jkr'

jkr_editor = JkrEditor(file_path=jkr_file_path)

with open(json_path, 'r') as f:
    jokers = json.load(f)

for index, joker_data in jkr_editor._data['cardAreas']['jokers']['cards'].items():
    code = joker_data['save_fields']['center']
    joker = dict(
        code=code,
        label=joker_data['label'],
        sort_id=joker_data.get('sort_id'),
        ability=joker_data['ability'],
        base_cost=joker_data['base_cost'],
        cost=joker_data['cost'],
        sell_cost=joker_data['sell_cost'],
        extra_cost=joker_data['extra_cost'],
    )

    jokers[code] = joker

with open(json_path, 'w') as f:
    f.write(json.dumps(jokers, indent=4))

with open(dat_path, 'wb') as fr:
    fr.write(compress_data(
        data=open(json_path, 'rb').read(),
        encryption_key=DATA_ENCRYPTION_KEY
    ))


