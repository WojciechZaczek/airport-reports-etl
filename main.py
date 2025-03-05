from transform.transform_utils import TransformUtils

""" Checking and testing classes"""

from extract.strategies.inflot_extract_strategy import InflotExtractStrategy
from extract.strategies.total_table_extract_strategy import TotalTableExtractStrategy
from transform.strategies.gus_a1.gus_a1_transform_strategy import A1TransformStrategy
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

transformer = A1TransformStrategy(inflot_report_df, total_report_df)

# a1_transform_strategy = A1TransformStrategy(inflot_report_df)
# transformer = Transform(
#     a1_transform_strategy
# )
# transformer.run()
transformer.fill_cargo_from_total()


transformer.df_total.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test_total.xlsx", index=False)
# transformer.prepare_columns()
# transformer.add_pax_onboard_column()
# transformer.create_new_columns()
# print(transformer.df_a1.info())
# transformer.remove_unnecessary_rows()
# transformer.remove_unnecessary_columns()
# transformer.aggregate_report()
# transformer.modify_AD_data()
# transformer.add_static_data()
# transformer.add_date_columns()
# transformer.format_remaining_data()
# transformer.reorder_columns()
# transformer.df_a1.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test.xlsx", index=False)
# # transformer.run()
# # transformer_b1()