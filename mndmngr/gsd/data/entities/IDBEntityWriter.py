from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData


T = TypeVar("T", bound=IDBEntityData)


class IDBEntityWriter(ABC, Generic[T]):
    @abstractmethod
    def write(self, entity: IDBEntity[T]) -> None:
        pass
