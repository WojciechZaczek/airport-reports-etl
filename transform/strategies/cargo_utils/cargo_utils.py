import pandas as pd
from transform.strategies.cargo_utils.cargo_config import (
    CARGO_DROP,
    CARGO_AIRLINEC_MAPPING,
    CARGO_PAIRPORT_MAPPING,
    MONTHS_MAPPING
)


class CargoData:
    def __init__(self, cargo_table: pd.DataFrame) -> None:
        """
        Initialize CargoData with a raw DataFrame.
        :param cargo_table: Raw Excel data containing multi-level headers and monthly cargo info.
        """
        self.cargo_df: pd.DataFrame = cargo_table

    def _preparing_multiindex_columns(self) -> None:
        """
        Converts first few header rows into a MultiIndex and prepares the cargo DataFrame.
        """
        headers = self.cargo_df.iloc[1:4].copy()
        data = self.cargo_df.iloc[4:].copy().reset_index(drop=True)

        headers = headers.fillna(method="ffill", axis=0)
        multi_cols = list(zip(*headers.values))

        self.cargo_df = pd.DataFrame(data.values, columns=pd.MultiIndex.from_tuples(multi_cols))

    def _trim_at_razem_zgr(self) -> None:
        """
        Trims the DataFrame to only include columns before the first occurrence of 'RAZEM ZAGRANICZNY'.
        """
        trim_idx = None
        for i, col in enumerate(self.cargo_df.columns):
            if any("RAZEM ZGR" in str(level).upper() for level in col):
                trim_idx = i
                break

        if trim_idx is not None:
            self.cargo_df = self.cargo_df.iloc[:, :trim_idx]

    def _drop_columns(self, drop_column: list[str]) -> pd.DataFrame:
        """
        Removes unwanted columns based on keywords.
        :param drop_column: List of keywords to drop from MultiIndex columns.
        :return: Filtered DataFrame.
        """
        drop_column_upper = [k.upper() for k in drop_column]

        def should_drop(col):
            return any(any(k in str(level).upper() for k in drop_column_upper) for level in col)

        filtered_cols = [col for col in self.cargo_df.columns if not should_drop(col)]
        self.cargo_df = self.cargo_df.loc[:, filtered_cols]
        return self.cargo_df

    def _filter_by_period_(self, year: int, month: int) -> None:
        """
        Filters the DataFrame by a given year and month.
        :param year: Year to filter by.
        :param month: Month to filter by.
        """
        roman_month = MONTHS_MAPPING.get(month)
        colnames = self.cargo_df.columns

        rok_idx = next((i for i, col in enumerate(colnames) if str(col[2]).upper() == "ROK"), None)
        miesiac_idx = next((i for i, col in enumerate(colnames) if str(col[2]).upper() == "MIESIĄC"), None)

        rok_values = self.cargo_df.iloc[:, rok_idx].astype(str)
        miesiac_values = self.cargo_df.iloc[:, miesiac_idx].astype(str).str.upper()

        mask = (rok_values == str(year)) & (miesiac_values == roman_month)
        self.cargo_df = self.cargo_df[mask].reset_index(drop=True)

    def _drop_empty_columns_for_selected_row(self) -> pd.DataFrame:
        """
        Drops columns with empty values in the first row.
        """
        row = self.cargo_df.iloc[0]
        non_empty_cols = row[row.notna() & (row.astype(str).str.strip() != '')].index
        self.cargo_df = self.cargo_df.loc[:, non_empty_cols]
        return self.cargo_df

    def _transpose_to_records(self) -> None:
        """
        Transposes the DataFrame so each row becomes a cargo record.
        """
        self.cargo_df = self.cargo_df.T.reset_index()
        self.cargo_df.columns = ['AIRLINEC', 'PAIRPORT', 'AD', 'FREIGHT ON BOARD']

    def _finalize_transposed_data(self) -> None:
        """
        Drops unused header rows and normalizes freight column.
        """
        self.cargo_df = self.cargo_df.drop(index=[0, 1]).reset_index(drop=True)
        self.cargo_df['FREIGHT ON BOARD'] = pd.to_numeric(self.cargo_df['FREIGHT ON BOARD'], errors='coerce') / 1000

    def _normalize_and_aggregate(self) -> None:
        """
        Normalizes values and aggregates data by AIRLINEC, PAIRPORT and AD.
        """
        ad_mapping = {'IMPORT': 1, "Import": 1, 'EXPORT': 2, 'Export': 2}
        self.cargo_df['AD'] = self.cargo_df['AD'].map(ad_mapping)
        self.cargo_df["PAIRPORT"] = self.cargo_df["PAIRPORT"].map(CARGO_PAIRPORT_MAPPING)
        self.cargo_df["AIRLINEC"] = self.cargo_df["AIRLINEC"].map(CARGO_AIRLINEC_MAPPING)

        self.cargo_df = self.cargo_df.groupby(['AIRLINEC', 'PAIRPORT', 'AD'], as_index=False).agg({
            'FREIGHT ON BOARD': 'sum'
        })

    def run(self, year: int, month: int) -> pd.DataFrame:
        """
        Orchestrates the full transformation process for the cargo data.
        :param year: Year to filter the data by.
        :param month: Month to filter the data by.
        :return: Transformed and aggregated cargo DataFrame.
        """
        self._preparing_multiindex_columns()
        self._drop_columns(CARGO_DROP)
        self._trim_at_razem_zgr()
        self._filter_by_period_(year, month)
        self._drop_empty_columns_for_selected_row()
        self._transpose_to_records()
        self._finalize_transposed_data()
        self._normalize_and_aggregate()

        self.cargo_df.to_excel(r"D:\Raporty\cargo.xlsx", index=False)

        return self.cargo_df
