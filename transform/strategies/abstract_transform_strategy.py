from abc import ABC, abstractmethod


class TransformStrategy(ABC):
    @abstractmethod
    def transform(self):
        """
        This is an abstract method that should be implemented by subclasses.

        :return: None
        """
        pass
