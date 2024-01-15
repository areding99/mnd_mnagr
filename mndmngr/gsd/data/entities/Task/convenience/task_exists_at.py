from mndmngr.gsd.data.queries.PathDBQuery import PathDBQuery


def task_exists_at(path: str) -> bool:
    query = PathDBQuery()
    query.set_query_args(path)
    res = query.run()

    return res is not None
