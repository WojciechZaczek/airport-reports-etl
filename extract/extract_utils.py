import datetime
import os
import pandas as pd
import shutil
from typing import Union


class ExtractUtils:
    """
    Utility class for handling file operations such as copying and loading data.
    """

    @staticmethod
    def create_timestamp() -> int:
        """
        Generate a timestamp for file naming.

        :return: Integer representing the current timestamp
        """
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def copy_file(source: str, destination_folder: str) -> Union[str, None]:
        """
        Copy a file to the destination folder with a timestamped filename.

        - Checks if the file exists before copying.
        - Creates a new filename with a timestamp to prevent overwriting.
        - Copies the file to the specified directory.

        :param source: The full path to the source file.
        :param destination_folder: The directory where the file will be copied.
        :return: The path of the copied file, or an error message if the file does not exist.
        """
        if not os.path.isfile(source):
            return f"Error, file in location {source} does not exist"

        filename, file_extension = os.path.splitext(os.path.basename(source))
        new_filename = f"{filename}_{ExtractUtils.create_timestamp()}{file_extension}"
        destination_path = os.path.join(destination_folder, new_filename)
        shutil.copy2(source, destination_path)

        print(f"File {new_filename} has been download to {destination_folder}")
        return destination_path

    @staticmethod
    def load_to_data_frame(destination_path: str) -> pd.DataFrame:
        """
        Load an Excel file into a Pandas DataFrame.

        :param sheet_name:
        :param destination_path: The full path to the Excel file.
        :return: A Pandas DataFrame containing the loaded data.
        """
        return pd.read_excel(destination_path)
