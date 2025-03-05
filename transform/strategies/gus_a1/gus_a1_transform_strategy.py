import pandas as pd
from transform.strategies.gus_a1.gus_a1_cargo_utils import CargoData
from transform.strategies.abstract_transform_strategy import TransformStrategy
from transform.strategies.gus_a1.gus_a1_config import REPORT_MAPPINGS, REPORTS_ROWS, FLIGHT_TYPES,REPORTS_COLUMNS
from transform.transform_utils import TransformUtils


class A1TransformStrategy(TransformStrategy):
    """
    Strategy class for transforming data into the A1 report format.
    """
    def __init__(self, df_inflot: pd.DataFrame, df_total: pd.DataFrame) -> None:
        """
        Initializes the transformation strategy with the input DataFrame.

        :param df: Original Pandas DataFrame containing raw data.
        """
        self.df_total = df_total
        self.df_inflot = df_inflot
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
        mapping = REPORT_MAPPINGS
        self.df_a1 = self.df_inflot
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
        self.df_a1["PAX ON BOARD"] = self.df_a1["TTL"].fillna(0) + self.df_a1["Infant"].fillna(0)
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
        self.df_a1["FLIGHT"] = self.df_a1['AD']
        return self.df_a1

    def remove_unnecessary_rows(self) -> pd.DataFrame:
        """
        Remove unnecessary rows based on the type of flight.

        This method filters out rows that do not belong to the predefined flight types
        required for the A1 report. It uses a predefined mapping (`REPORTS_ROWS["A1"]`)
        to determine which flight types should be retained.

        Returns:
        pd.DataFrame: A filtered DataFrame containing only relevant flight types.
        """
        col_filter = "Typ rejsu"
        self.df_a1 = TransformUtils.keep_relevant_rows(self.df_a1, col_filter, REPORTS_ROWS)
        return self.df_a1

    def remove_unnecessary_columns(self) -> pd.DataFrame:
        """
        Remove unnecessary columns from the DataFrame.
        This method ensures that only the relevant columns required for the A1 report
        are retained in the DataFrame. It filters the DataFrame using a predefined list
        of column names.

        Returns:
        pd.DataFrame: A DataFrame containing only the necessary columns for the report.
        """
        mapping = [
        "PAIRPORT",
        "AD",
        "SCHEDNS",
        "PASSFREIGH",
        "AIRLINEC",
        "AIRCRAFTTY",
        "PAX ON BOARD",
        "SEATAV",
        "FLIGHT"
    ]
        self.df_a1 = TransformUtils.keep_relevant_columns(self.df_a1, mapping)
        return self.df_a1

    def aggregate_report(self) -> pd.DataFrame:
        """
        Aggregates the report by summing PAX_ON_BOARD and SEATAV,
        and counting occurrences of AD (stored in a new column FLIGHT).

        Returns:
        pd.DataFrame: The aggregated DataFrame.
        """
        self.df_a1 = self.df_a1.groupby(
            ["PAIRPORT", "FLIGHT", "AD", "SCHEDNS", "PASSFREIGH", "AIRLINEC", "AIRCRAFTTY"],
            as_index=False
        ).agg({
            "PAX ON BOARD": sum,
            "SEATAV": sum,
            "FLIGHT": "count"
        })
        return self.df_a1

    def modify_AD_data(self) -> pd.DataFrame:
        """
        Modify the 'AD' column values based on a predefined mapping.

        This method replaces values in the 'AD' column using a dictionary mapping.
        'P' is replaced with 1, and 'O' is replaced with 2.

        Returns:
            pd.DataFrame: The updated DataFrame with modified 'AD' column values.
        """
        mapping = {"P": 1, "O": 2}
        self.df_a1 = TransformUtils.replacing_data(self.df_a1, 'AD', mapping)
        return self.df_a1

    def fill_cargo_from_total(self) -> pd.DataFrame:
        total = CargoData(self.df_total)
        self.df_total = total.preparing_columns()
        self.df_total = total.forward_fill_labels()
        return self.df_total

    def format_remaining_data(self) -> pd.DataFrame:
        """
           Handles missing values in the DataFrame by applying a predefined strategy.

           This method processes the remaining data in `df_a1` by using `TransformUtils.handle_null_values()`
           to replace or remove NaN values, ensuring data consistency before final export.

           Returns:
           pd.DataFrame: The cleaned DataFrame with handled missing values.
           """

        self.df_a1 = TransformUtils.handle_null_values(self.df_a1)
        return self.df_a1

    def add_static_data(self) -> pd.DataFrame:
        """
        Adds static values to specific columns in the DataFrame.

        Returns:
        pd.DataFrame: The updated DataFrame with static values added.
        """
        self.df_a1["TABLE"] = 'A1'
        self.df_a1["COUNTRY"] = 'EP'
        self.df_a1["RAIRPORT"] = 'EPGD'
        self.df_a1["FREIGHT ON BOARD"] = 0
        return self.df_a1

    def add_date_columns(self) -> pd.DataFrame:
        """
        Extracts a reference date from the dataset and assigns year and period columns.

        This method retrieves a middle-record date from the original dataset (`df`)
        using `TransformUtils.get_middle_record_data()` and populates two new columns:

        - "YEAR": Extracted as a two-digit year from the reference date.
        - "PERIOD": Extracted as the month number from the reference date.


        Returns:
        pd.DataFrame: The updated DataFrame with static values added.

        """

        date = TransformUtils.get_middle_record_data(self.df_inflot)
        self.df_a1["YEAR"] = date.strftime("%y")
        self.df_a1["PERIOD"] = date.month
        return self.df_a1

    def reorder_columns(self) -> pd.DataFrame:
        """
        Ensures the correct column order in the final DataFrame.

        This method reorders `df_a1` columns based on a predefined list,
        ensuring consistency with expected report structure.

        Returns:
        pd.DataFrame: The DataFrame with columns arranged in the correct order.
        """
        self.df_a1 = self.df_a1[REPORTS_COLUMNS]
        return self.df_a1

    def transform(self):
        pass
