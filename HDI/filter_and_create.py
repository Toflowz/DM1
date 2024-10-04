import pandas as pd

#df = pd.read_excel("hdr-data.ods").to_csv("hdr-data.csv")

df_data = pd.read_csv("data.csv")

df_data = df_data[['Location', 'Period', 'Dim1ValueCode', 'FactValueNumeric']]
df_data = df_data[df_data['Dim1ValueCode'] == 'SEX_BTSX']
df_data = df_data[['Location', 'Period', 'FactValueNumeric']]
df_data = df_data.sort_values(by=['Location', 'Period'])

#          Location  Period  FactValueNumeric
# 10910  Afghanistan    2000              7.71
# 10364  Afghanistan    2001              7.89

df_data.to_csv('df_data_filtered.csv', index=False)

df_hdi = pd.read_csv("hdr-data.csv")
# contains 'world', 'least developed countries' etc in country, to clean if used without the merge
df_hdi = df_hdi[['country', 'indicator', 'year', 'value']]
df_hdi = df_hdi.rename(columns={'country': 'Location', 'year': 'Period'})

df_merged = df_data.merge(right=df_hdi, how='inner', on=['Location', 'Period'])

print(df_hdi.columns)

print(df_merged)
df_merged.to_csv('df_merged.csv', index=False)