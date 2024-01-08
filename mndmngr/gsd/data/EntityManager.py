from typing import Type

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData
from mndmngr.gsd.data.entities.IDBEntityDataParser import IDBEntityDataParser
from mndmngr.gsd.data.queries.IDBMultiQuery import IDBMultiQuery
from mndmngr.gsd.data.queries.IDBQuery import IDBQuery


def get(
    Entity: Type[IDBEntity],
    parser: IDBEntityDataParser,
    query: IDBQuery,
    *query_args: str,
) -> IDBEntity | None:
    res = query.run(*query_args)

    if res is None:
        return None

    [path, data] = res
    parsed: IDBEntityData = parser.parse(data)

    return Entity(path, parsed)


def get_many(
    Entity: Type[IDBEntity],
    parser: IDBEntityDataParser,
    query: IDBMultiQuery,
    *query_args: str,
) -> list[IDBEntity] | None:
    result = query.run(*query_args)

    if result is None:
        return None

    return [Entity(path, parser.parse(data)) for [path, data] in result.items()]


def write(data: IDBEntityData) -> None:
    pass


def create(data: IDBEntityData) -> None:
    pass


def delete(data: IDBEntityData) -> None:
    pass


def delete_at_path(path: str) -> None:
    pass
