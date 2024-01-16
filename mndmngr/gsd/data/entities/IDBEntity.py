from abc import ABC, abstractmethod
import os
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData


class IDBEntity(ABC):
    _rel_path: str
    _data: IDBEntityData | None

    @abstractmethod
    def __init__(self, path: str, data: IDBEntityData | None = None):
        pass

    @staticmethod
    @abstractmethod
    def get_entity_path_rel() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_entity_path_absolute() -> str:
        pass

    @staticmethod
    def get_entity_path_prefix() -> str:
        return os.environ["PROJECT_ROOT"]

    def get_absolute_path(self) -> str:
        return IDBEntity.get_entity_path_prefix() + self.get_path()

    def get_data(self) -> IDBEntityData | None:
        return self._data

    def set_data(self, data: IDBEntityData) -> None:
        self._data = data

    def get_path(self) -> str:
        return self._rel_path

    def is_initialized(self) -> bool:
        return self._data is not None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IDBEntity):
            return NotImplemented

        if not isinstance(self, other.__class__):
            return NotImplemented

        print(other.__class__)

        return self.get_path() == other.get_path()
