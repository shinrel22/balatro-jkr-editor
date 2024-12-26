import os

from config import ROOT_PATH

TMP_DIR = os.path.join(ROOT_PATH, 'tmp')
if not os.path.exists(TMP_DIR):
    try:
        os.makedirs(TMP_DIR)
    except FileExistsError as e:
        print('TMP existed', e)

DATA_DIR = os.path.join(ROOT_PATH, 'data')
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
    except FileExistsError as e:
        print('DATA existed', e)

