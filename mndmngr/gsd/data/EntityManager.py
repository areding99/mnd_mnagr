import os
from pathlib import Path
from typing import Type

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData
from mndmngr.gsd.data.entities.IDBEntityDataParser import IDBEntityDataParser
from mndmngr.gsd.data.entities.IDBEntityWriter import IDBEntityWriter
from mndmngr.gsd.data.queries.IDBMultiQuery import IDBMultiQuery
from mndmngr.gsd.data.queries.IDBQuery import IDBQuery
from mndmngr.gsd.data.queries.PathDBQuery import PathDBQuery


def get(
    Entity: Type[IDBEntity],
    parser: IDBEntityDataParser,
    query: IDBQuery,
) -> IDBEntity | None:
    res = query.run()

    if res is None:
        return None

    [path, data] = res

    to_trim = Entity.get_entity_path_prefix()

    return Entity(path[len(to_trim) :], parser.parse(data))


def get_many(
    Entity: Type[IDBEntity],
    parser: IDBEntityDataParser,
    query: IDBMultiQuery,
) -> list[IDBEntity] | None:
    res = query.run()

    if res is None:
        return None

    to_trim = Entity.get_entity_path_prefix()
    res = {
        path[len(to_trim) :]: data
        for [path, data] in res.items()
        if path.startswith(to_trim)
    }
    return [Entity(path, parser.parse(data)) for [path, data] in res.items()]


def initialize(
    ent: IDBEntity,
    parser: IDBEntityDataParser,
) -> IDBEntity:
    if ent.is_initialized():
        return ent

    query = PathDBQuery()
    query.set_query_args(ent.get_absolute_path())

    res = query.run()

    if res is None:
        raise Exception("Entity not found at path: " + ent.get_absolute_path())

    data = parser.parse(res[1])

    ent.set_data(data)
    return ent


def write(ent: IDBEntity, writer: IDBEntityWriter) -> bool:
    try:
        writer.write(ent)
    except Exception as e:
        print("error writing ent: " + str(e))
        return False

    return True


def create(data: IDBEntityData) -> None:
    pass


def delete(data: IDBEntityData) -> None:
    pass


def delete_at_path(path: str) -> None:
    pass
