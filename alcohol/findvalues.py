import pandas as pd

alcohol_data = pd.read_csv('filtered_alcohol_data.csv')
suicide_data = pd.read_csv('filtered_suicide_data.csv')

merged_data = pd.merge(alcohol_data, suicide_data, on=['SpatialDimValueCode', 'Period'], how='inner', suffixes=('_alcohol', '_suicide'))

missing_alcohol = merged_data[merged_data['FactValueNumeric_alcohol'].isna()]
missing_suicide = merged_data[merged_data['FactValueNumeric_suicide'].isna()]

merged_data_cleaned = merged_data.dropna()
merged_data_cleaned.to_csv('cleaned_merged_data.csv', index=False)
