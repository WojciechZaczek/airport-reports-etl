from abc import ABC, abstractmethod


class ExtractStrategy(ABC):
    @abstractmethod
    def extract(self):
        """
        This is an abstract method that should be implemented by subclasses.
        :return: None
        """
        pass
