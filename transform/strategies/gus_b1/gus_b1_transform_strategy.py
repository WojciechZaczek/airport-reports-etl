import pandas as pd
from transform.strategies.abstract_transform_strategy import TransformStrategy
from transform.transform_utils import TransformUtils
from transform.strategies.gus_b1.gus_b1_config import REPORTS_COLUMNS


class B1TransformStrategy(TransformStrategy):
    """
    Strategy class for transforming data into the B1 report format.
    """

    def __init__(self, df_a1: pd.DataFrame) -> None:
        """
        Initializes the transformation strategy with the input DataFrame.

        :param df_a1: Pandas DataFrame containing transformed A1 report data.
        """
        self.df_b1 = df_a1

    def get_data(self) -> pd.DataFrame:
        """
        Returns the transformed DataFrame.

        :return: Pandas DataFrame containing the transformed B1 report data.
        """
        return self.df_b1


    def _change_columns_names(self) -> None:
        """
        Renames the column 'PAX ON BOARD' to 'PAX CARRIED'.

        This method ensures consistency with the required column naming convention in B1 reports.

        :return: Pandas DataFrame with updated column names.
        """
        self.df_b1 = self.df_b1.rename(columns={"PAX ON BOARD": "PAX CARRIED"})

    def _change_static_data(self) -> None:
        """
        Adds static values to specific columns required in the B1 report.

        - 'TABLE' is set to 'B1' to indicate the report type.

        :return: Pandas DataFrame with updated static values.
        """
        self.df_b1["TABLE"] = 'B1'

    def _delete_unnecessary_columns(self) -> None:
        """
        Removes columns that are not required in the B1 report.

        This method filters `df_b1` to retain only the columns specified in `REPORTS_COLUMNS`.

        :return: Pandas DataFrame containing only the relevant columns.
        """
        self.df_b1 = TransformUtils.keep_relevant_columns(self.df_b1, REPORTS_COLUMNS)

    def _reorder_columns(self) -> None:
        """
        Ensures the correct column order in the final DataFrame.

        This method reorders `df_b1` columns based on a predefined list,
        ensuring consistency with the expected B1 report structure.

        :return: Pandas DataFrame with columns arranged in the correct order.
        """
        self.df_b1 = self.df_b1[REPORTS_COLUMNS]

    def run(self):
        """
        Executes the entire transformation process step by step.
        This method ensures that all necessary transformations are applied in the correct order.

        :return: Fully transformed DataFrame ready for reporting.
        """
        self._change_columns_names()
        self._change_static_data()
        self._delete_unnecessary_columns()
        self._reorder_columns()
        return self.df_b1


