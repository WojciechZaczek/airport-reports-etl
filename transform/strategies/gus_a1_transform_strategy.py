import pandas as pd
from transform.strategies.abstract_transform_strategy import TransformStrategy
from utils.mapping import REPORT_MAPPINGS, REPORTS_COLUMNS, REPORTS_ROWS, FLIGHT_TYPES
from utils.transform_utils import TransformUtils


class A1TransformStrategy(TransformStrategy):
    """
    Strategy class for transforming data into the A1 report format.
    """
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the transformation strategy with the input DataFrame.

        :param df: Original Pandas DataFrame containing raw data.
        """
        self.df = df
        self.df_a1 = pd.DataFrame()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the transformed DataFrame.

        :return: Pandas DataFrame containing the transformed A1 report data.
        """
        return self.df_a1

    def prepare_columns(self) -> pd.DataFrame:
        """
        Cleans and renames columns in the DataFrame to match the A1 report structure.

        - Copies data from the original DataFrame (`self.df`) to `self.df_a1`
        - Renames columns using predefined mappings (`REPORT_MAPPINGS["A1"]`)

        :return: Pandas DataFrame with renamed columns.
        """
        mapping = REPORT_MAPPINGS["A1"]
        self.df_a1 = self.df
        self.df_a1 = TransformUtils.rename_columns(self.df_a1, mapping)
        return self.df_a1

    def add_pax_onboard_column(self) -> pd.DataFrame:
        """
        Creates a new column 'PAX ON BOARD' by summing 'TTL' (total passengers) and 'Infant'.

        - 'TTL' represents the total number of passengers onboard (excluding infants).
        - 'Infant' represents the number of infants onboard.
        - The sum of these two values gives the total count of passengers onboard, including infants.

        :return: Pandas DataFrame with the added 'PAX ON BOARD' column.
        """
        self.df_a1["PAX ON BOARD"] = self.df_a1["TTL"] + self.df_a1["Infant"]
        return self.df_a1

    def create_new_columns(self) -> pd.DataFrame:
        """
        Creates two new columns: 'PASSFREIGH' and 'SCHEDNS' based on the flight type.

        - 'PASSFREIGH': Categorizes flights into passenger (1) or cargo (2).
        - 'SCHEDNS': Categorizes flights as scheduled (1) or non-scheduled (2).
        - Uses a predefined mapping (`FLIGHT_TYPES`) to assign values.

        Steps:
        1. Maps the 'Typ rejsu' column to the corresponding values for 'PASSFREIGH'.
        2. Maps the 'Typ rejsu' column to the corresponding values for 'SCHEDNS'.

        :return: Pandas DataFrame with added 'PASSFREIGH' and 'SCHEDNS' columns.
        """
        self.df_a1["PASSFREIGH"] = self.df_a1["Typ rejsu"].map(FLIGHT_TYPES["PASSFREIGH"])
        self.df_a1["SCHEDNS"] = self.df_a1["Typ rejsu"].map(FLIGHT_TYPES["SCHEDNS"])
        print(self.df_a1.head())
        return self.df_a1

    def remove_unnecessary_rows(self):
        col_filter = "Typ rejsu"
        self.df_a1 = TransformUtils.keep_relevant_rows(self.df_a1, col_filter, REPORTS_ROWS["A1"])
        return self.df_a1

    def remove_unnecessary_columns(self):
        mapping = [
        "PAIRPORT",
        "AD",
        "SCHEDNS",
        "PASSFREIGH",
        "AIRLINEC",
        "AIRCRAFTTY",
        "PAX ON BOARD",
        "SEATAV",
    ]
        self.df_a1 = TransformUtils.keep_relevant_columns(self.df_a1, mapping)
        return self.df_a1

    def aggregate_report(self):
        self.df_a1 = self.df_a1.groupby(
            ["PAIRPORT", "AD", "AIRLINEC", "AIRCRAFTTY", "PASSFREIGH", "SCHEDNS"]
        ).agg({
            "PAX ON BOARD": "sum",
            "SEATAV": "sum",
            "AD": ("FLIGHT", "count")
        }).reset_index()
        return self.df_a1

    def modify_AD_data(self):
        mapping = {"P": 1, "O": 2}
        self.df_a1 = TransformUtils.replacing_data(self.df_a1, 'AD', mapping)
        return self.df_a1

    def fill_cargo_from_total(self):
        pass

    def format_remaining_data(self):
        self.df_a1 = TransformUtils.handle_null_values(self.df_a1)
        return self.df_a1

    def add_constant_data(self):
        pass






