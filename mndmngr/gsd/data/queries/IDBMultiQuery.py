from abc import ABC, abstractmethod


class IDBMultiQuery(ABC):
    @abstractmethod
    def run(self) -> dict[str, list[str]]:
        pass

    def set_query_args(self, *args: str) -> None:
        self._query_args = args
