from abc import ABC, abstractmethod

class idatabase(ABC):

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def last_insert_id(self, table: str):
        pass

    def get_by_field(self, table: str, field: str, value: str):
        pass