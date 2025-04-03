import os
import pandas as pd
from load.load_utils import LoadUtils
from load.strategies.abstract_load_strategy import LoadStrategy


class ExcelLoadStrategy(LoadStrategy):
    def __init__(self, df: pd.DataFrame, table_type: str, year: int, month: int):
        """
        Initializes the Excel load strategy.

        :param df: DataFrame to be saved.
        :param table_type: Report type (e.g., "A1", "B1", "C1").
        :param year: Full year (e.g., 2024).
        :param month: Month as an integer (1–12).
        """
        self.df = df
        self.table_type = table_type
        self.year = int(str(year)[-2:])
        self.month = month

    def load(self, save_path: str) -> str:
        """
        Saves the DataFrame as an Excel file with the proper filename format.

        :param save_path: Directory where the file should be saved.
        :return: Full path to the saved Excel file.
        """
        filename = LoadUtils.generate_report_filename(self.table_type, self.year, self.month)
        full_path = os.path.join(save_path, f"{filename}.xlsx")
        self.df.to_excel(full_path, index=False)
        print(f" Saved report {self.table_type} to: {full_path}")
        return full_path
