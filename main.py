

""" Checking and testing classes"""

from extract.strategies.inflot_extract_strategy import InflotExtractStrategy
from transform.strategies.gus_a1_transform_strategy import A1TransformStrategy
import os


file_path = "D:\inflot.xlsx"
print(f"Checking file path: {file_path}")

if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
else:
    print(f"File {file_path} exists.")

strategy = InflotExtractStrategy(file_path)

inflot_report_df = strategy.retrive_data()

transformer = A1TransformStrategy(inflot_report_df)



transformer.prepare_columns()
transformer.add_pax_onboard_column()
transformer.create_new_columns()
print(transformer.df_a1.info())
transformer.remove_unnecessary_rows()
transformer.remove_unnecessary_columns()
# transformer.modify_AD_data()
# transformer.aggregate_report()
# transformer.format_remaining_data()
print(transformer.df_a1.info())
print(transformer.df_a1.head())
