import os
import zlib
import json
from copy import deepcopy

from src.constants.cards import CARD_NEGATIVE_EDITION
from src.models.joker import Joker
from src.models.tag import Tag
from src.utils.lua_parser import lua_parser
from src.utils import decompress_data, compress_data
from src.constants.dirs import TMP_DIR
from src.constants.data import TAGS


class JkrEditor(object):
    def __init__(self, file_path: str):
        self._file_path = file_path

        self._raw_data: bytes = decompress_data(
            data=open(file_path, 'rb').read(),
            wbits=-zlib.MAX_WBITS
        )

        self._data: dict = lua_parser.decode(self._raw_data.decode().replace('return', ''))

        # write data to json file for better dev
        with open(
                os.path.join(TMP_DIR, 'current.json'),
                mode='w',
                encoding='utf-8'
        ) as f:
            f.write(json.dumps(self._data, indent=4))

        self._tags: list[Tag] = self._load_tags()

        self._jokers: list[Joker] = self._load_jokers()

        self._money: float = self._data['GAME']['dollars']

        self._joker_slots: int = self._data['GAME']['max_jokers']

    def _load_jokers(self) -> list[Joker]:
        result = []

        for index, joker_data in self._data['cardAreas']['jokers']['cards'].items():
            result.append(Joker(
                data=joker_data,
                index=int(index),
            ))

        return sorted(result, key=lambda joker: joker.index)

    def _load_tags(self) -> list[Tag]:
        result = []

        for index, tag_data in self._data['tags'].items():
            result.append(Tag(data=tag_data, index=int(index)))

        return sorted(result, key=lambda tag: tag.index)

    @staticmethod
    def compress(data: bytes) -> bytes:
        compressor = zlib.compressobj(level=zlib.Z_BEST_COMPRESSION, wbits=-zlib.MAX_WBITS)
        compressed_data = compressor.compress(data) + compressor.flush()
        return compressed_data

    @property
    def data(self) -> dict:

        result = deepcopy(self._data)

        # save tags
        tags = dict()
        game_tags = dict()
        for tag in self._tags:
            tags[tag.index] = tag.data
            game_tags[tag.index] = '"MANUAL_REPLACE"'
        result['tags'] = tags

        # save jokers
        jokers = dict()
        for joker in self._jokers:
            jokers[joker.index] = joker.data
        result['cardAreas']['jokers']['cards'] = jokers

        # save money
        result['GAME']['dollars'] = self._money

        # save joker slots
        result['GAME']['max_jokers'] = self._joker_slots
        result['cardAreas']['jokers']['config']['card_limit'] = self._joker_slots
        result['cardAreas']['jokers']['config']['temp_limit'] = self._joker_slots

        return result

    def save(self, output_path: str = None, create_backup: bool = False):

        if not output_path:
            output_path = self._file_path

        if create_backup:
            with open(f'{self._file_path}.backup', 'wb') as f:
                f.write(compress_data(
                    data=self._raw_data,
                    level=zlib.Z_BEST_COMPRESSION,
                    wbits=-zlib.MAX_WBITS
                ))

        data_as_lua = f'return {lua_parser.encode(self.data)}'
        compressed_data = compress_data(
            data=data_as_lua.encode(),
            level=zlib.Z_BEST_COMPRESSION,
            wbits=-zlib.MAX_WBITS
        )

        with open(output_path, 'wb') as f:
            f.write(compressed_data)

    @property
    def money(self) -> float:
        return self._money

    def set_money(self, value: float):
        self._money = value

    @property
    def tags(self) -> list[Tag]:
        return self._tags

    def add_tag(self, code: str) -> Tag:
        index = 1
        tally = 438

        if self.tags:
            index = self.tags[-1].index + 1
            tally = self.tags[-1].tally + 1

        tag = Tag.init(
            code=code,
            index=index,
            tally=tally
        )

        self._tags.append(tag)

        return tag

    def clear_tags(self):
        self._tags = []

    @property
    def jokers(self) -> list[Joker]:
        return self._jokers

    def add_joker(self, code: str, edition_code: str = None) -> Joker:

        joker_data = Joker.generate_data(code=code)
        index = 1
        if self._jokers:
            index = self.jokers[-1].index + 1

        joker = Joker(
            data=joker_data,
            index=index,
        )
        if edition_code:
            joker.change_edition(edition_code=edition_code)

        self._jokers.append(joker)

        if joker.edition and joker.edition.code == CARD_NEGATIVE_EDITION:
            self._joker_slots += 1

        return joker
