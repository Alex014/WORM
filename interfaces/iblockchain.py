from abc import ABC, abstractmethod

class iblockchain(ABC):

    @abstractmethod
    def loadDirectData(self):
        pass

    @abstractmethod
    def loadUrlData(self):
        pass