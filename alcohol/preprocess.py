import pandas as pd

df_se = pd.read_csv('suicide_data.csv')

df_se_filtered = df_se[['SpatialDimValueCode', 'Period', 'Dim1ValueCode', 'FactValueNumeric']]

df_se_filtered = df_se_filtered[df_se_filtered['Dim1ValueCode'] == 'SEX_BTSX']
df_se_filtered = df_se_filtered[['SpatialDimValueCode', 'Period', 'FactValueNumeric']]
df_se_filtered = df_se_filtered.sort_values(by='Period', ascending=False)
df_se_filtered.to_csv('filtered_suicide_data.csv', index=False)

df_al = pd.read_csv('alcohol_data.csv')

df_al_filtered = df_al[['SpatialDimValueCode', 'Period', 'Dim1ValueCode', 'FactValueNumeric']]
df_al_filtered = df_al_filtered[df_al_filtered['Dim1ValueCode'] == 'ALCOHOLTYPE_SA_TOTAL']
df_al_filtered = df_al_filtered[['SpatialDimValueCode', 'Period', 'FactValueNumeric']]
df_al_filtered = df_al_filtered[df_al_filtered['Period'] >= 2000]
df_al_filtered = df_al_filtered[df_al_filtered['Period'] <= 2019]
df_al_filtered = df_al_filtered.sort_values(by='Period', ascending=False)

df_al_filtered.to_csv('filtered_alcohol_data.csv', index=False)