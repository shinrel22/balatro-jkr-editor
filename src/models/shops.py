from copy import deepcopy

from src.bases.models import DataModel, BaseModel


class JokerShop(DataModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._max_slots: int = self._data['config']['card_limit']

    @property
    def max_slots(self) -> int:
        return self._max_slots

    def set_max_slots(self, value: int) -> None:
        self._max_slots = value

    @property
    def data(self) -> dict:
        result = deepcopy(self._data)

        # save max slots
        result['config']['card_limit'] = self._max_slots
        result['config']['temp_limit'] = self._max_slots

        return result
