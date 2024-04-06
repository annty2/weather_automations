import os


class SQLQuery:
    _current_dir = os.path.dirname(__file__)

    def __init__(self, file_name: str):
        self._filename = os.path.join(self._current_dir, file_name)

    def read(self,*args, **kwargs):
        with open(self._filename, 'r') as file:
            return file.read().format(**kwargs)
