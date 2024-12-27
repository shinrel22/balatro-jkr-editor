from copy import deepcopy

from src.bases.models import DataModel, BaseModel


class Tag(DataModel):
    index: int = 1
    tally: int = 438
    code: str | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.code = self._data['key']

    @classmethod
    def generate_data(cls, code: str, tally: int) -> dict:
        result = {
            'key': code,
            'tally': tally,
            'ability': {
                'orbital_hand': "[poker hand]"
            },
        }

        return result

    @property
    def data(self) -> dict:
        result = deepcopy(self._data)

        result['key'] = self.code
        result['tally'] = self.tally

        return result
