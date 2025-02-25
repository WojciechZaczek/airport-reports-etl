from transform.transform_utils import TransformUtils

""" Checking and testing classes"""

from extract.strategies.inflot_extract_strategy import InflotExtractStrategy
from transform.strategies.gus_a1.gus_a1_transform_strategy import A1TransformStrategy
import os


file_path = r"C:\Users\wojci\OneDrive\Pulpit\airport\inflot.xlsx"
print(f"Checking file path: {file_path}")

if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
else:
    print(f"File {file_path} exists.")

strategy = InflotExtractStrategy(file_path)

inflot_report_df = strategy.retrive_data()

transformer = A1TransformStrategy(inflot_report_df)

# a1_transform_strategy = A1TransformStrategy(inflot_report_df)
# transformer = Transform(
#     a1_transform_strategy
# )
# transformer.run()


transformer.prepare_columns()
transformer.add_pax_onboard_column()
transformer.create_new_columns()
print(transformer.df_a1.info())
transformer.remove_unnecessary_rows()
transformer.remove_unnecessary_columns()
transformer.aggregate_report()
transformer.modify_AD_data()
transformer.add_static_data()
transformer.add_date_columns()
transformer.df_a1.to_excel(r"C:\Users\wojci\PycharmProjects\airport-reports-etl\boxes\GUS\reports\test.xlsx", index=False)
# transformer.format_remaining_data()
# transformer.correct_columns_order()
# # transformer.run()
# # transformer_b1()