""" Checking and testing classes"""

from extract.strategies.inflot_extract_strategy import InflotExtractStrategy
from extract.strategies.total_table_extract_strategy import TotalTableExtractStrategy
from transform.strategies.gus_a1.gus_a1_transform_strategy import A1TransformStrategy
from transform.strategies.gus_b1.gus_b1_transform_strategy import B1TransformStrategy
from transform.strategies.gus_c1.gus_c1_transform_strategy import C1TransformStrategy
from load.strategies.excel_load_strategy import ExcelLoadStrategy
import os

file_path_total = r"D:\Raporty\TABELA_TOTAL_AKTUALNA.xlsx"

file_path_inflot = r"D:\Raporty\luty25.xls"
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

c1_transformer = C1TransformStrategy(inflot_report_df, total_report_df)
c1_transformer.run()

year, month = a1_transformer.get_year_month()

loader_a1 = ExcelLoadStrategy(a1_transformer.run(), "A1", year, month)
loader_a1.load(r'C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports')

loader_b1 = ExcelLoadStrategy(b1_transformer.run(), "B1", year, month)
loader_b1.load(r'C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports')

loader_c1 = ExcelLoadStrategy(c1_transformer.run(),"C1", year, month)
loader_c1.load(r'C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports')



a1_transformer.df_a1.to_excel(r"D:\Raporty\A1, B1, C1\EP2502A1.xlsx", index=False)
c1_transformer.df_c1.to_excel(r"D:\Raporty\A1, B1, C1\EP2502C1.xlsx", index=False)
b1_transformer.df_b1.to_excel(r"D:\Raporty\A1, B1, C1\EP2502B1.xlsx", index=False)
