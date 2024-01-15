from abc import ABC, abstractmethod


class IDBQuery(ABC):
    @abstractmethod
    def run(self) -> tuple[str, list[str]] | None:
        pass

    def set_query_args(self, *args: str) -> None:
        self._query_args = args
