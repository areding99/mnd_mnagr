from abc import ABC, abstractmethod
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData


class IDBEntityDataParser(ABC):
    @abstractmethod
    def parse(self, data: list[str]) -> IDBEntityData:
        pass
