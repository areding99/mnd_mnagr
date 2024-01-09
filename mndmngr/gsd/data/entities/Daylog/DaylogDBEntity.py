import os, sys, dotenv
from mndmngr.gsd.data.entities.Daylog.DaylogEntityData import DaylogEntityData

if __name__ == "__main__":
    dotenv.load_dotenv()
    sys.path.append(os.environ["PROJECT_ROOT"])

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity


class DaylogDBEntity(IDBEntity):
    def __init__(self, path: str, data: DaylogEntityData | None = None):
        self._path = path
        self._data = data

    @staticmethod
    def get_entity_path() -> str:
        return os.environ["DAILY_LOG_PATH"]
