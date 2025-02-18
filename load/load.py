from load.strategies.abstract_load_strategy import LoadStrategy


class Load:
    def __init__(self, strategy: LoadStrategy) -> None:
        """
        Initialize the Load class.

        Parameters:
        strategy (LoadStrategy): The strategy used for data load.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> LoadStrategy:
        """
        :return: The current load strategy being employed
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: LoadStrategy) -> None:
        """
        :param strategy: The loading strategy to be used, an instance of LoadStrategy.
        :return: None
        """
        self._strategy = strategy

    def load_data(self):
        """
        :return: Load the data to database by the current strategy.
        """
        self._strategy.load()



