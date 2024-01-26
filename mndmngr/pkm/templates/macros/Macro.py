from abc import ABC, abstractmethod
from datetime import date


class Macro(ABC):
    def __init__(self, date: date, file_path_rel: str, file_path_abs: str):
        self.date = date
        self.file_path_rel = file_path_rel
        self.file_path_abs = file_path_abs

    @abstractmethod
    def resolve(self) -> str:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass
