import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


merged_data = pd.read_csv('cleaned_suicide_health_expenditure.csv')

merged_data['Value'] = pd.to_numeric(merged_data['Value'], errors='coerce')
merged_data['Health_Expenditure'] = pd.to_numeric(merged_data['Health_Expenditure'], errors='coerce')

merged_data_clean = merged_data.dropna(subset=['Value', 'Health_Expenditure'])

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Health_Expenditure', y='Value', data=merged_data_clean)

plt.title('Correlation Between Health Expenditure and Suicide Rates', fontsize=16)
plt.xlabel('Health Expenditure (% of GDP)', fontsize=12)
plt.ylabel('Suicide Rates (per 100,000 population)', fontsize=12)

plt.show()