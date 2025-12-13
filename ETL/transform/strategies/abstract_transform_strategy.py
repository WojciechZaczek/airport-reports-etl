from abc import ABC, abstractmethod
import pandas as pd


class TransformStrategy(ABC):
    @abstractmethod
    def get_data(self):
        """
        This is an abstract method that should be implemented by subclasses.

        :return: None
        """
    @abstractmethod
    def run(self) -> pd.DataFrame:
        """
        Executes all transformation steps in the correct order.

        :return: The fully transformed DataFrame.
        """
        pass