import os
import pandas as pd
import shutil
from typing import Optional
from transform.strategies.abstract_transform_strategy import TransformStrategy


class GusTransformStrategy(TransformStrategy):
    def __init__(self, inflot_report, total_table):
        self.inflot_report = inflot_report
        self.total_table = total_table
