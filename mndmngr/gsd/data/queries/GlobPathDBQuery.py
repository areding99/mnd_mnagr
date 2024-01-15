import glob
from mndmngr.gsd.data.queries.IDBMultiQuery import IDBMultiQuery


class GlobPathDBQuery(IDBMultiQuery):
    def run(self) -> dict[str, list[str]]:
        [
            glob_path,
        ] = self._query_args

        paths = glob.glob(glob_path)

        if len(paths) == 0:
            print("could not find any files at: " + glob_path)
            return {}

        return {path: self._read_lines(path) for path in paths}

    def _read_lines(self, path: str) -> list[str]:
        with open(path, "r") as f_io:
            return f_io.readlines()
