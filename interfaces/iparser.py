from abc import ABC, abstractmethod


class iparser(ABC):

    def __init__(self, parent_id: int):
        self.parent_id = parent_id

    @abstractmethod
    def parse(self, data: dict):
        pass

    @abstractmethod
    def init_db(self):
        pass