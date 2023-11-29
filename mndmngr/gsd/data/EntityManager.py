from abc import ABC, abstractmethod
from typing import Type


class IDBEntityData:
    pass


class TaskEntityData(IDBEntityData):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class IDBEntity(ABC):
    _path: str
    _data: IDBEntityData

    @abstractmethod
    def __init__(self, path: str, data: IDBEntityData):
        pass

    def get_data(self) -> IDBEntityData:
        return self._data

    def get_path(self) -> str:
        return self._path


class TaskDBEntity(IDBEntity):
    def __init__(self, path: str, data: TaskEntityData):
        self._path = path
        self._data = data


class IDBQuery(ABC):
    @abstractmethod
    def run(self, arg: str) -> dict[str, list[str]]:
        pass


class PathDBQuery(IDBQuery):
    def run(self, arg: str) -> dict[str, list[str]]:
        return {"path": ["nameSample", "descriptionSample"]}


class IDBEntityDataParser(ABC):
    @abstractmethod
    def parse(self, data: list[str]) -> IDBEntityData:
        pass


class TaskDBEntityDataParser(IDBEntityDataParser):
    def parse(self, data: list[str]) -> IDBEntityData:
        return TaskEntityData(data[0], data[1])


def get(
    Entity: Type[IDBEntity], query: IDBQuery, parser: IDBEntityDataParser
) -> IDBEntity:
    data = query.run("arg")
    path = ""
    for key in data:
        path = key

    parsed: IDBEntityData = parser.parse(data[path])

    return Entity(path, parsed)


def write(data: IDBEntityData) -> None:
    pass


def create(data: IDBEntityData) -> None:
    pass


def delete(data: IDBEntityData) -> None:
    pass


def delete_at_path(path: str) -> None:
    pass


print(get(TaskDBEntity, PathDBQuery(), TaskDBEntityDataParser()))
