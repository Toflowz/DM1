import scipy.stats as stats
import pandas as pd

merged_data_cleaned = pd.read_csv('cleaned_merged_data.csv')
correlation_pearson = merged_data_cleaned['FactValueNumeric_alcohol'].corr(merged_data_cleaned['FactValueNumeric_suicide'])

correlation_spearman, p_value_spearman = stats.spearmanr(merged_data_cleaned['FactValueNumeric_alcohol'], merged_data_cleaned['FactValueNumeric_suicide'])

print(f"Pearson Correlation: {correlation_pearson}")
print(f"Spearman Correlation: {correlation_spearman}, p-value: {p_value_spearman}")