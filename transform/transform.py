from transform.strategies.abstract_transform_strategy import TransformStrategy


class Transform:

    def __init__(self, strategy: TransformStrategy):
        """
        :param strategy: An instance of the Strategy class that defines the algorithm to be used.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> TransformStrategy:
        """
        :return: The current strategy object, representing the approach or algorithm to be used in a certain context.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: TransformStrategy) -> None:
        """
        :param strategy: The strategy instance to be set.
        :return: None
        """
        self._strategy = strategy

    def run(self):
        """
        :return:  Get data transform by the current strategy
        """
        return self._strategy.transform()
