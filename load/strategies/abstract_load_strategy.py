from abc import ABC, abstractmethod


class LoadStrategy(ABC):
    @abstractmethod
    def load(self):
        """
             This is an abstract method that should be implemented by subclasses.

             :return: None
             """
        pass


