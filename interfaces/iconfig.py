from abc import ABC, abstractmethod

class iconfig:

    @abstractmethod
    def get_config(self, filename: str) -> dict:
        pass