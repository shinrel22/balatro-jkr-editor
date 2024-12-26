import json


class Error(Exception):
    code = 'UnknownError'
    message = None
    meta = {}

    def __init__(self,
                 code: str = None,
                 message: str = None,
                 meta: dict = None):

        self.message = message

        if not code:
            code = self.__class__.__name__

        self.code = code

        self.meta = meta or {}

    def output(self) -> dict:
        data = {
            'message': self.message,
            'code': self.code,
            'meta': self.meta
        }
        return data

    def __str__(self):
        return json.dumps(self.output())
