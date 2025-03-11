import pandas as pd
from transform.strategies.abstract_transform_strategy import TransformStrategy
from transform.transform_utils import TransformUtils
from transform.strategies.gus_c1.gus_c1_config import REPORTS_COLUMNS, REPORT_MAPPINGS, REPORTS_ROWS, \
    MAPPING_TMY, MAPPING_A1_TYPE


class C1TransformStrategy(TransformStrategy):
    """
    Strategy class for transforming data into the C1 report format.
    """

    def __init__(self, df_inflot: pd.DataFrame) -> None:
        """
        Initializes the transformation strategy with the input DataFrame.
        """
        self.df_inflot = df_inflot
        self.df_c1 = pd.DataFrame()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the transformed DataFrame..
        """
        return self.df_c1

    def prepare_columns(self) -> pd.DataFrame:
        """
        Cleans and renames columns in the DataFrame to match the C1 report structure.

        - Copies data from `df_inflot` to `df_c1`.
        - Renames columns using predefined mappings (`REPORT_MAPPINGS`).

        :return: Pandas DataFrame with renamed columns.
        """
        mapping = REPORT_MAPPINGS
        self.df_c1 = self.df_inflot
        self.df_c1 = TransformUtils.rename_columns(self.df_c1, mapping)
        return self.df_c1

    def add_columns(self) -> pd.DataFrame:
        """
        Adds new columns required for the C1 report.

        - 'PAX' is calculated as the sum of 'TTL' (total passengers) and 'Infant'.
        - 'AIRCRAFTM' and 'AIRCRAFTMY' are initialized as copies of 'FLIGHT'.
        - 'FREIGHT' is initialized with a default value of 0.

        :return: Updated Pandas DataFrame.
        """
        self.df_c1["PAX"] = self.df_c1["TTL"].fillna(0) + self.df_c1["Infant"].fillna(0)
        self.df_c1["AIRCRAFTM"] = self.df_c1["FLIGHT"]
        self.df_c1["AIRCRAFTMY"] = self.df_c1["FLIGHT"]
        self.df_c1["FREIGHT"] = 0
        return self.df_c1

    def remove_unnecessary_rows(self) -> pd.DataFrame:
        """
        Removes unnecessary rows from the dataset based on the flight type.

        - Filters the dataset using predefined `REPORTS_ROWS`.

        :return: Pandas DataFrame with only relevant rows.
        """
        col_filter = "Typ rejsu"
        self.df_c1 = TransformUtils.keep_relevant_rows(self.df_c1, col_filter, REPORTS_ROWS)
        return self.df_c1

    def remove_unnecessary_columns(self) -> pd.DataFrame:
        """
        Removes unnecessary columns from the DataFrame, retaining only those
        required for the C1 report.

        :return: Pandas DataFrame containing only necessary columns.
        """
        mapping = ["FLIGHT", "AIRLINEC", "TRANSITPAX", "AIRCRAFTM", "AIRCRAFTMY", "FREIGHT", "PAX", "Typ rejsu"]
        self.df_c1 = TransformUtils.keep_relevant_columns(self.df_c1, mapping)
        return self.df_c1

    @staticmethod
    def create_df_with_operation_type(df: pd.DataFrame, col_filter: str, filter_values: list) -> pd.DataFrame:
        """
        Creates an aggregated DataFrame filtered by a specific flight type.

        - Filters the input DataFrame based on `col_filter` and `filter_values`.
        - Aggregates passenger, transit, aircraft, and freight data per airline.

        :param df: The input Pandas DataFrame.
        :param col_filter: Column used to filter data (e.g., "Typ rejsu").
        :param filter_values: List of values to retain in the filtering column.
        :return: Aggregated Pandas DataFrame.
        """
        df = TransformUtils.keep_relevant_rows(df, col_filter, filter_values)
        df = df.groupby(["AIRLINEC"], as_index=False).agg({
            "PAX": sum,
            "TRANSITPAX": sum,
            "AIRCRAFTM": "count",
            "AIRCRAFTMY": "count",
            "FREIGHT": "sum"
        })
        return df

    def generate_a1_type_df(self) -> pd.DataFrame:
        """
        Generates an aggregated DataFrame for A1 report types.

        - Filters flights belonging to passenger and cargo categories.
        - Aggregates data per airline.

        :return: Aggregated Pandas DataFrame.
        """

        return self.create_df_with_operation_type(self.df_c1, "Typ rejsu", MAPPING_A1_TYPE)

    def generate_tmy_type_df(self) -> pd.DataFrame:
        """
        Generates an aggregated DataFrame for TMY report types.

        - Filters flights categorized as General Aviation, Technical, or Medical.
        - Initializes missing values for PAX and AIRCRAFTM.

        :return: Aggregated Pandas DataFrame.
        """

        df_tmy = self.create_df_with_operation_type(self.df_c1, "Typ rejsu", MAPPING_TMY)
        df_tmy["PAX"] = 0
        df_tmy["AIRCRAFTM"] = 0
        return df_tmy

    def combine_aggregated_data(self) -> pd.DataFrame:
        """
        Combines aggregated passenger and general aviation data.

        - Generates data for general aviation flights.
        - Merges specific cases from the 'Sanitarny' category into the main dataset.
        - Ensures missing aircraft types are mapped from a reference dataset.

        :return: Combined Pandas DataFrame.
        """
        df_tmy = self.generate_tmy_type_df()
        df_tm = self.create_df_with_operation_type(self.df_c1, "Typ rejsu", ["Sanitarny"])

        aircraft_mapping = dict(zip(df_tm["AIRLINEC"], df_tm["AIRCRAFTMY"]))
        df_tmy["AIRCRAFTM"] = df_tmy["AIRLINEC"].map(aircraft_mapping).fillna(df_tmy["AIRCRAFTM"])

        self.df_c1 = pd.concat([self.generate_a1_type_df(), df_tmy], ignore_index=True)
        return self.df_c1

    def add_static_data(self) -> pd.DataFrame:
        """
        Adds static values to specific columns in the DataFrame.

        :return: Updated Pandas DataFrame with static values.
        """
        self.df_c1["TABLE"] = "C1"
        self.df_c1["COUNTRY"] = "EP"
        self.df_c1["RAIRPORT"] = "EPGD"
        return self.df_c1

    def add_date_columns(self) -> pd.DataFrame:
        """
        Extracts a reference date from the dataset and assigns year and period columns.

        - "YEAR": Extracted as a two-digit year from the reference date.
        - "PERIOD": Extracted as the month number from the reference date.

        :return: Updated Pandas DataFrame.
        """
        date = TransformUtils.get_middle_record_data(self.df_inflot)
        self.df_c1["YEAR"] = date.strftime("%y")
        self.df_c1["PERIOD"] = date.month
        return self.df_c1

    def reorder_columns(self) -> pd.DataFrame:
        """
        Ensures the correct column order in the final DataFrame.

        :return: Pandas DataFrame with columns arranged in the correct order.
        """
        self.df_c1 = self.df_c1[REPORTS_COLUMNS]
        return self.df_c1
