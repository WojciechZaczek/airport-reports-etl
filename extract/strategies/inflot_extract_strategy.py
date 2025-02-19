import datetime
import os
import pandas as pd
import shutil
from typing import Optional
from extract.strategies.abstract_extract_strategy import ExtractStrategy
from utils.extract_utils import ExtractUtils


class InflotExtractStrategy(ExtractStrategy):
    """Extractor for Inflot report."""

    def __init__(self, file_path):
        self.inbox_path = "boxes\\inflot\\inbox"
        self.file_path = file_path
        self.df = None

    def retrive_data(self):
        destination_path = ExtractUtils.copy_file(self.file_path, self.inbox_path)
        if "Error" in destination_path:
            return destination_path

        self.df = ExtractUtils.load_to_data_frame(destination_path)
        return self.df



