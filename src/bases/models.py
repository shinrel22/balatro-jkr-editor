from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def to_dict(self, **kwargs) -> dict:
        return self.model_dump(**kwargs)


class DataModel(BaseModel):
    _data: dict

    def __init__(self, data: dict, **kwargs):
        super().__init__(**kwargs)

        self._data = data

    @property
    def data(self) -> dict:
        return self._data
