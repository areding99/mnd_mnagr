from abc import ABC, abstractmethod
from mndmngr.gsd.data.entities.IDBEntity import IDBEntity


class IDBEntityWriter(ABC):
    @abstractmethod
    def write(self, entity: IDBEntity) -> None:
        pass
