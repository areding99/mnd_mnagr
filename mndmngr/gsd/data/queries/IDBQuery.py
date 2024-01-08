from abc import ABC, abstractmethod


class IDBQuery(ABC):
    @abstractmethod
    def run(self, *args: str) -> tuple[str, list[str]] | None:
        pass
