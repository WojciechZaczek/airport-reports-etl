import datetime
import os
import pandas as pd
import shutil
from typing import Optional


class ExtractUtils:
    """Utility class for handling file operations."""

    @staticmethod
    def create_timestamp():
        """
        Generate a timestamp for file naming.
        """
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def copy_file(source: str, destination_folder: str):
        """
        Copy a file to the destination folder with a timestamped filename.
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
    def load_to_data_frame(destination_path):
        """
        Load an Excel file into a pandas DataFrame.
        """
        return pd.read_excel(destination_path)
