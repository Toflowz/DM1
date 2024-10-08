import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

merged_data_cleaned = pd.read_csv('cleaned_merged_data.csv')

unique_countries = merged_data_cleaned['SpatialDimValueCode'].unique()
colors = plt.cm.get_cmap('Set1', len(unique_countries))

# Create a dictionary to map country codes to colors
color_dict = {country: colors(i) for i, country in enumerate(unique_countries)}

# Create the scatter plot
plt.figure(figsize=(10, 6))

for country in unique_countries:
    subset = merged_data_cleaned[merged_data_cleaned['SpatialDimValueCode'] == country]
    plt.scatter(subset['FactValueNumeric_alcohol'], subset['FactValueNumeric_suicide'], label=country, color=color_dict[country], s=100, alpha=0.8)

# Add labels and title
plt.xlabel('Alcohol Consumption (per capita)')
plt.ylabel('Suicide Rate (per 100k population)')
plt.title('Scatter Plot of Alcohol Consumption vs Suicide Rate by Country')

# Add a legend with country labels
plt.legend(title='Country Code', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()