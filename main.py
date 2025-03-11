from transform.transform_utils import TransformUtils

""" Checking and testing classes"""

from extract.strategies.inflot_extract_strategy import InflotExtractStrategy
from extract.strategies.total_table_extract_strategy import TotalTableExtractStrategy
from transform.strategies.gus_a1.gus_a1_transform_strategy import A1TransformStrategy
from transform.strategies.gus_b1.gus_b1_transform_strategy import B1TransformStrategy
from transform.strategies.gus_c1.gus_c1_transform_strategy import C1TransformStrategy
import os

file_path_total = r"C:\Users\wojci\OneDrive\Pulpit\airport\TABELA_TOTAL_AKTUALNA.xlsx"

file_path_inflot = r"C:\Users\wojci\OneDrive\Pulpit\airport\inflot.xlsx"
print(f"Checking file path: {file_path_inflot}")

if not os.path.exists(file_path_inflot):
    print(f"File {file_path_inflot} does not exist.")
else:
    print(f"File {file_path_inflot} exists.")


strategy_inflot = InflotExtractStrategy(file_path_inflot)
inflot_report_df = strategy_inflot.retrive_data()

strategy_total = TotalTableExtractStrategy(file_path_total)
total_report_df = strategy_total.retrive_data()

a1_transformer = A1TransformStrategy(inflot_report_df, total_report_df)
a1_transformer.run()


b1_transformer = B1TransformStrategy(a1_transformer.df_a1)
b1_transformer.run()


c1_transformer = C1TransformStrategy(inflot_report_df)
c1_transformer.run()


a1_transformer.df_total.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test_total.xlsx", index=False)
a1_transformer.df_a1.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test_a1.xlsx", index=False)
c1_transformer.df_c1.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test_c1.xlsx", index=False)
b1_transformer.df_b1.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test_b1.xlsx", index=False)