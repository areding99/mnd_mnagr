from typing import TypeVar
from typing import Type

from mndmngr.gsd.data.entities.IDBEntity import IDBEntity
from mndmngr.gsd.data.entities.IDBEntityData import IDBEntityData
from mndmngr.gsd.data.entities.IDBEntityDataParser import IDBEntityDataParser
from mndmngr.gsd.data.entities.IDBEntityWriter import IDBEntityWriter
from mndmngr.gsd.data.queries.IDBMultiQuery import IDBMultiQuery
from mndmngr.gsd.data.queries.IDBQuery import IDBQuery
from mndmngr.gsd.data.queries.PathDBQuery import PathDBQuery

T = TypeVar("T", bound=IDBEntity)


def get(
    Entity: Type[T],
    parser: IDBEntityDataParser,
    query: IDBQuery,
) -> T | None:
    res = query.run()

    if res is None:
        return None

    [path, data] = res

    to_trim = Entity.get_entity_path_prefix()

    return Entity(path[len(to_trim) :], parser.parse(data))


def get_many(
    Entity: Type[T],
    parser: IDBEntityDataParser,
    query: IDBMultiQuery,
) -> list[T] | None:
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
    ent: T,
    parser: IDBEntityDataParser,
) -> T:
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


def write(ent: T, writer: IDBEntityWriter) -> bool:
    try:
        writer.write(ent)
    except Exception as e:
        print("error writing ent: " + str(e))
        return False

    return True
