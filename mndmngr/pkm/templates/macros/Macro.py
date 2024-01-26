from abc import ABC, abstractmethod
from datetime import datetime


class Macro(ABC):
    def __init__(
        self, file_name: str, file_path_rel: str, file_path_abs: str, datetime: datetime
    ):
        self.file_name = file_name
        self.file_path_rel = file_path_rel
        self.file_path_abs = file_path_abs
        self.datetime = datetime

    @abstractmethod
    def resolve(self) -> str:
        pass

    @abstractmethod
    def get_key(self) -> str:
        pass
