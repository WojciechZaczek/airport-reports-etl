import pandas as pd


class CargoData:
    def __init__(self, cargo_table: pd.DataFrame):
        self.cargo_df = cargo_table

    def preparing_columns(self):
        year_col_index = self.cargo_df.columns[self.cargo_df.iloc[0].astype(str).str.contains("ROK", na=False)].tolist()[0]
        last_valid_column = self.cargo_df.columns[self.cargo_df.iloc[0].astype(str).str.contains("RAZEM ZGR", na=False)].tolist()[0]
        self.cargo_df = self.cargo_df.iloc[:, year_col_index:last_valid_column]
        return self.cargo_df

    def preparing_rows(self):
        pass

    def forward_fill_labels(self):
        for row in range(4):
            for col in range(1, self.cargo_df.shape[1]):
                if pd.isna(self.cargo_df.iloc[row, col]) or self.cargo_df.iloc[row, col] == "":
                    self.cargo_df.iloc[row, col] = self.cargo_df.iloc[row, col - 1]
        return self.cargo_df

    def mod_labels(self):
        pass

    def mod_by_melt(self):
        pass

    def normalize_cargo_data(self):
        # change structure of dataframe
        # atomized view for each column/ pivon or unpivot
        pass

    def run(self):
        self.preparing_columns()
        self.forward_fill_labels()
