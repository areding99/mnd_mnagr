import os
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity


class DaylogDBEntity(IDBEntity[DaylogEntityData]):
    def __init__(self, path: str, data: IDBEntityData | None = None):
        if (data is not None) and (not isinstance(data, DaylogEntityData)):
            raise TypeError("data must be of type DaylogEntityData")

        self._rel_path = path
        self._data = data

    @staticmethod
    def get_entity_path_rel() -> str:
        return os.environ["DAILY_LOG_REL_PATH"]

    @staticmethod
    def get_entity_path_absolute() -> str:
        return os.environ["DAILY_LOG_PATH"]
