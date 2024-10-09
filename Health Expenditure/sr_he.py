import pandas as pd
import re

# Load the two CSV files into pandas dataframes
suicide_rates = pd.read_csv('Health Expenditure/suicide rates.csv')
health_expenditure = pd.read_csv('Health Expenditure/health expenditure.csv')

# Drop unnecessary columns from the suicide_rates dataframe
columns_to_drop = ['IndicatorCode', 'Indicator', 'ParentLocationCode', 'ParentLocation', 'Location type', 
                   'Period type', 'IsLatestYear', 'ValueType', 'Dim1 type','Dim1ValueCode', 
                   'DateModified', 'Language', 'FactComments', 'FactValueTranslationID', 'Dim2 type', 'Dim2',
                   'Dim2ValueCode', 'Dim3 type', 'Dim3', 'Dim3ValueCode', 'DataSourceDimValueCode', 'DataSource',
                   'FactValueNumericPrefix', 'FactValueUoM', 'FactValueNumericLowPrefix', 
                   'FactValueNumericLow', 'FactValueNumericHighPrefix','FactValueNumericHigh' ]
suicide_rates = suicide_rates.drop(columns=columns_to_drop)

# Filter suicide_rates to only include rows where Dim1 (Sex) is for both sexes
suicide_rates_filtered = suicide_rates[suicide_rates['Dim1'].str.contains('Both sexes', case=False, na=False)]

# Use .loc to modify the 'Period' column in the filtered DataFrame
suicide_rates_filtered.loc[:, 'Period'] = suicide_rates_filtered['Period'].astype(int)

health_expenditure_melted = health_expenditure.melt(id_vars=['Countries', 'Indicators'], 
                                                    var_name='Year', value_name='Health_Expenditure')

health_expenditure_melted['Year'] = pd.to_numeric(health_expenditure_melted['Year'], errors='coerce')
health_expenditure_melted = health_expenditure_melted.dropna(subset=['Year'])
health_expenditure_melted['Year'] = health_expenditure_melted['Year'].astype(int)

merged_data = pd.merge(suicide_rates_filtered, 
                       health_expenditure_melted, 
                       left_on=['Location', 'Period'], 
                       right_on=['Countries', 'Year'], 
                       how='left')

merged_data = merged_data.drop(columns=['Indicators', 'Countries', 'Year'])
merged_data.to_csv('Health Expenditure/merged_suicide_health_expenditure.csv', index=False)
merged_data = pd.read_csv('Health Expenditure/merged_suicide_health_expenditure.csv')

# Function to extract the numeric value before the brackets
def extract_numeric(value):
    # Use regex to find the numeric part before the brackets
    match = re.match(r'([0-9]*\.?[0-9]+)', str(value))
    if match:
        return match.group(1)
    return value  # Return the original value if no match

merged_data['Value'] = merged_data['Value'].apply(extract_numeric)
merged_data = merged_data.drop(columns=['Location', 'Dim1', 'Value'])
merged_data.to_csv('Health Expenditure/cleaned_suicide_health_expenditure.csv', index=False)

print(merged_data.head())

#cleaned_data = pd.read_csv('Health Expenditure/cleaned_suicide_health_expenditure.csv')
#cleaned_data = cleaned_data.drop(columns=['Location', 'Dim1', 'Value'])
#cleaned_data.to_csv(