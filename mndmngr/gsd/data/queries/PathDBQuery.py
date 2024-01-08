import os
from mndmngr.gsd.data.queries.IDBQuery import IDBQuery


class PathDBQuery(IDBQuery):
    def run(self, *args: str) -> tuple[str, list[str]] | None:
        [
            path,
        ] = args

        if not os.path.exists(path):
            print("could not find task at: " + path)
            return None

        with open(path, "r") as f_io:
            return (path, f_io.readlines())

        return None
