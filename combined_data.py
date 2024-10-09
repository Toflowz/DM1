import pandas as pd

nurses_df = pd.read_csv("Mental Health Availability/data/nurses.csv").drop(columns="Unnamed: 0")
psych_df = pd.read_csv("Mental Health Availability/data/psychiatrists.csv").drop(columns="Unnamed: 0")
alc_df = pd.read_csv("alcohol/cleaned_merged_data.csv")
hdi_df = pd.read_csv("HDI/df_merged_DimValueCode.csv")
he_df = pd.read_csv("Health Expenditure/cleaned_suicide_health_expenditure.csv")

combined_df = nurses_df.merge(psych_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(alc_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(hdi_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(he_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])

print(combined_df.head(10))