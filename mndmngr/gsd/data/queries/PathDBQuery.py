import os
from mndmngr.gsd.data.queries.IDBQuery import IDBQuery


class PathDBQuery(IDBQuery):
    def run(self) -> tuple[str, list[str]] | None:
        [
            path,
        ] = self._query_args

        if not os.path.exists(path):
            print("could not find file at: " + path)
            return None

        with open(path, "r") as f_io:
            return (path, f_io.readlines())
