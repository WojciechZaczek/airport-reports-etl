from typing import Union
import pandas as pd
from extract.strategies.abstract_extract_strategy import ExtractStrategy
from extract.extract_utils import ExtractUtils


class TotalTableExtractStrategy(ExtractStrategy):
    """
    Extractor for Total Table report.

    This class is responsible for:
    - Copying the given file to the designated inbox directory.
    - Loading the copied file into a Pandas DataFrame.
    """

    def __init__(self, file_path: str):
        """
        Initializes the extractor with the file path.

        :param file_path: The full path to the Excel file that needs to be processed.
        """

        self.inbox_path = "boxes\\total_table\\inbox"
        self.file_path = file_path
        self.df = None

    def retrive_data(self) -> Union[pd.DataFrame, str]:
        """
        Retrieves data by copying the file and loading it into a Pandas DataFrame.

        Steps:
        1. Copies the file from `self.file_path` to `self.inbox_path` using `ExtractUtils.copy_file()`.
        2. If copying fails (returns an error message), the function returns the error.
        3. Otherwise, loads the copied file into a DataFrame.

        :return: A Pandas DataFrame containing the extracted data or an error message if the file cannot be copied.
        """
        destination_path = ExtractUtils.copy_file(self.file_path, self.inbox_path)
        if "Error" in destination_path:
            return destination_path

        self.df = pd.read_excel(destination_path, sheet_name="CARGO", header=None)
        return self.df
