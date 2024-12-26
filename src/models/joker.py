from copy import deepcopy

from src.bases.models import DataModel, BaseModel
from src.constants.data import JOKERS
from src.constants.cards import (CARD_FOIL_EDITION, CARD_NEGATIVE_EDITION, CARD_POLYCHROME_EDITION,
                                 CARD_HOLOGRAPHIC_EDITION, CARD_EDITIONS)
from src.bases.errors import Error


class BaseJoker(BaseModel):
    code: str
    label: str
    ability: dict
    sort_id: int = None
    cost: int
    sell_cost: int
    base_cost: int
    extra_cost: int = 0


class JokerEdition(BaseModel):
    code: str


class Joker(DataModel):
    index: int

    _edition: JokerEdition = None
    _base: BaseJoker = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._base = self._load_base()

        self._edition = self._load_edition()

    def _load_edition(self) -> JokerEdition | None:
        edition_data = self._data.get('edition')
        if edition_data is None:
            return None
        code = edition_data['type']
        return JokerEdition(code=code)

    def _load_base(self) -> BaseJoker:
        code = self._data['save_fields']['center']

        base_data = JOKERS.get(code)
        if base_data is None:
            # update new joker to file
            base_data = dict(
                code=code,
                label=self._data['label'],
                ability=self._data['ability'],
                sell_cost=self._data['sell_cost'],
                cost=self._data['cost'],
                base_cost=self._data['base_cost'],
                extra_cost=self._data['extra_cost'],
            )
            JOKERS[code] = base_data

        base_joker = BaseJoker(**base_data)

        return base_joker

    @property
    def label(self) -> str:
        return self._base.label

    @property
    def edition(self) -> JokerEdition | None:
        return self._edition

    def change_edition(self, edition_code: str) -> None:

        if edition_code not in CARD_EDITIONS:
            raise Error(
                message=f'Unknown edition code: {edition_code}',
            )

        self._edition = JokerEdition(code=edition_code)

    @property
    def data(self) -> dict:
        new_data = deepcopy(self._data)

        if self._edition:
            edition = dict(
                type=self._edition.code,
            )
            if self._edition.code == CARD_NEGATIVE_EDITION:
                edition['negative'] = True
            elif self._edition.code == CARD_FOIL_EDITION:
                edition['foil'] = True
                edition['chips'] = 50
            elif self._edition.code == CARD_POLYCHROME_EDITION:
                edition['polychrome'] = True
                edition['x_mult'] = 1.5
            elif self._edition.code == CARD_HOLOGRAPHIC_EDITION:
                edition['holographic'] = True
                edition['s_mult'] = 10
            else:
                raise Error(
                    message=f'Unknown edition code: {self._edition.code}',
                )
            new_data['edition'] = edition
        else:
            new_data.pop('edition', None)

        new_data['rank'] = self.index

        return new_data

    @classmethod
    def generate_data(cls, code: str) -> dict:
        result = {
            "sprite_facing": "front",
            "facing": "front",
            "save_fields": {
                "center": code
            },
            "base": {
                "nominal": 0,
                "suit_nominal": 0,
                "face_nominal": 0,
                "times_played": 0
            },
            "bypass_discovery_center": True,
            "params": {
                "discover": False,
                "bypass_discovery_center": True,
                "bypass_discovery_ui": True,
                "bypass_back": {
                    "y": 2,
                    "x": 4
                }
            },
            "debuff": False,
            "bypass_discovery_ui": True,
            "bypass_lock": True,
            "added_to_deck": True
        }

        base_data = JOKERS.get(code)
        if not base_data:
            raise Error(
                message=f'Unsupported joker code: {code}',
            )

        result.update(base_data)

        return result




