from typing import Optional
from extract.strategies.abstract_extract_strategy import ExtractStrategy
from utils.extract_utils import ExtractUtils


class TotalTableExtractStrategy(ExtractStrategy):
    """Extractor for Total tablereport."""

    def __init__(self, file_path):
        self.inbox_path = "boxes\\total_table\\inbox"
        self.file_path = file_path
        self.df = None

    def retrive_data(self):
        destination_path = ExtractUtils.copy_file(self.file_path, self.inbox_path)
        if "Error" in destination_path:
            return destination_path

        self.df = ExtractUtils.load_to_data_frame(destination_path)
        return self.df
