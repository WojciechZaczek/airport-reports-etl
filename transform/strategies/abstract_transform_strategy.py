from abc import ABC, abstractmethod


class TransformStrategy(ABC):
    @abstractmethod
    def get_data(self):
        """
        This is an abstract method that should be implemented by subclasses.

        :return: None
        """
