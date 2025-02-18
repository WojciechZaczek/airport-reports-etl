import datetime
import os
import shutil
from typing import Optional
from extract.strategies.abstract_extract_strategy import ExtractStrategy


class InflotExtractStrategy(ExtractStrategy):
    """
       Extractor class for extracting data from Inflot report.

    """

    def __init__(self, file_path):
        self.inbox_path = "boxes\\inflot\\inbox"
        self.file_path = file_path

    @staticmethod
    def create_timestamp():
        return int(datetime.datetime.now().timestamp())

    def retrive_data(self):
        return self._copy_file(self.file_path, self.inbox_path)

    def _copy_file(self, source: str, destination_folder: str):
        if not os.path.isfile(source):
            return f"Error, file in location {source} does not exist"

        filename, file_extension = os.path.splitext(os.path.basename(source))
        new_filename = f"{filename}_{self.create_timestamp()}{file_extension}"
        destination_path = os.path.join(destination_folder, new_filename)
        shutil.copy2(source, destination_path)

        return f"File {new_filename} has been download to {destination_folder}"
