from typing import Union


class Node:

    def __init__(self, *args: str, **kwargs: str):
        self._name = kwargs.get('name')
        self._path = kwargs.get('path')
        self._parent = kwargs.get('parent')
        self._type = kwargs.get('type')
        self._digest = kwargs.get('digest')

    def get_name(self) -> str:
        return self._name

    def get_path(self) -> str:
        return self._path

    def get_parent(self) -> str:
        return self._parent

    def get_type(self) -> str:
        return self._type

    def get_digest(self) -> Union[str, Exception]:
        if self.is_file():
            return self._digest
        else:
            raise Exception(f'Cannot get digest for directory {self.get_name()}')

    def is_file(self) -> bool:
        return self._type == 'file'
