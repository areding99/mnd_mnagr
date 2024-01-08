from abc import ABC, abstractmethod


class IDBMultiQuery(ABC):
    @abstractmethod
    def run(self, *args: str) -> dict[str, list[str]]:
        pass
