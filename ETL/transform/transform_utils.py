import datetime
import pandas as pd
import shutil
from typing import Optional


class TransformUtils:
    """Utility class for handling data transform operations."""

    @staticmethod
    def keep_relevant_columns(dataframe: pd.DataFrame, relevant_columns: list) -> pd.DataFrame:
        """
        Keep only relevant columns in the DataFrame.

        :param dataframe: Input DataFrame with various columns.
        :param relevant_columns: List of columns that must be present.
        :return: DataFrame containing only the relevant columns.
        :raises ValueError: If any required column is missing.
        """

        missing_columns = [col for col in relevant_columns if col not in dataframe.columns]
        if missing_columns:
            ValueError(f'Missing required columns in report: {missing_columns}')

        dataframe = dataframe[relevant_columns]
        return dataframe

    @staticmethod
    def keep_relevant_rows(dataframe: pd.DataFrame, column_filter: str, relevant_rows: list) -> pd.DataFrame:
        dataframe = dataframe[dataframe[column_filter].isin(relevant_rows)]
        return dataframe

    @staticmethod
    def rename_columns(dataframe: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        """
        Cleans column names by removing leading/trailing spaces and newline characters,
        then renames them based on the provided mapping.

        :param dataframe: Input Pandas DataFrame with original column names.
        :param mapping: Dictionary mapping old column names to new column names.
        :return: A new DataFrame with cleaned and renamed columns.
        """
        dataframe.columns = dataframe.columns.str.strip()
        dataframe.columns = dataframe.columns.str.replace(r"[\n]", " ", regex=True).str.strip()
        return dataframe.rename(columns=mapping)



    @staticmethod
    def replacing_data(dataframe: pd.DataFrame, column: str, mapping: dict) -> pd.DataFrame:
        dataframe[column] = dataframe[column].replace(mapping)
        return dataframe

    @staticmethod
    def handle_null_values(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        """
        dataframe = dataframe.fillna(0)
        return dataframe

    @staticmethod
    def get_middle_record_data(dataframe: pd.DataFrame) -> datetime:
        middle_index = len(dataframe) // 2
        first_column = dataframe.columns[0]
        mid_value = dataframe.loc[middle_index, first_column]
        mid_data = pd.to_datetime(mid_value)
        return mid_data









