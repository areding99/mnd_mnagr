import os, sys, dotenv
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity


class DaylogDBEntity(IDBEntity):
    def __init__(self, path: str, data: IDBEntityData | None = None):
        if (data is not None) and (not isinstance(data, DaylogEntityData)):
            raise TypeError("data must be of type DaylogEntityData")

        self._path = path
        self._data = data

    @staticmethod
    def get_entity_path() -> str:
        return os.environ["DAILY_LOG_PATH"]
