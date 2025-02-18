""" Checking and testing classes"""

from extract.strategies.total_table_extract_strategy import TotalExtractStrategy
import os


file_path = input("Write file path: ").strip('"')
print(f"Checking file path: {file_path}")

if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
else:
    print(f"File {file_path} exists.")

strategy = TotalExtractStrategy(file_path)

result = strategy.retrive_data()
print(result)
