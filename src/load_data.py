# import pandas as pd

# df = pd.read_excel("data/sample_superstore.xls")

# print("Column names:")
# print(df.columns.tolist())

# print("\nFirst 5 rows:")
# print(df.head())

import pandas as pd

xls = pd.ExcelFile("data/sample_superstore.xls")
print(xls.sheet_names)

people = pd.read_excel("data/sample_superstore.xls", sheet_name="People")
print(people.head())

returns = pd.read_excel("data/sample_superstore.xls", sheet_name="Returns")
print(returns.head())