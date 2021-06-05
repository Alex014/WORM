from abc import ABC, abstractmethod

class iloader(ABC):

    @abstractmethod
    def load(self, url: str):
        pass