import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from itertools import product
import matplotlib.pyplot as plt
import sklearn.cluster as cl
import sklearn.metrics as dv

nurses_df = pd.read_csv("Mental Health Availability/data/nurses.csv").drop(columns="Unnamed: 0")
psych_df = pd.read_csv("Mental Health Availability/data/psychiatrists.csv").drop(columns="Unnamed: 0")
alc_df = pd.read_csv("alcohol/cleaned_merged_data.csv")
hdi_df = pd.read_csv("HDI/df_merged_DimValueCode.csv")
he_df = pd.read_csv("Health Expenditure/cleaned_suicide_health_expenditure.csv")
homicide_df = pd.read_csv("Homocide_Support_programs/allDataCleaned.csv")

combined_df = nurses_df.merge(psych_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(alc_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(hdi_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(he_df, on=["SpatialDimValueCode", "Period", "FactValueNumeric"])
combined_df = combined_df.merge(homicide_df, on=["SpatialDimValueCode", "Period"]).drop(columns=["Unnamed: 0", "childHomeVisits","elderCare","partnerVioPrevention","youthPrograms"])
combined_df = combined_df[combined_df["indicator"] == "Human Development Index (value)"].drop(columns="indicator").reset_index()
combined_df = combined_df.rename(columns={"value": "HDI", "FactValueNumeric": "suicide_rate"})
combined_df = combined_df.drop(columns="index")
combined_df = combined_df.interpolate(method='linear')
combined_df.to_csv("complete_data.csv")

minmax_scaled = combined_df.copy()

info_columns = ["HealthAvailVal_nurse",
                  "suicide_rate",
                  "HealthAvailVal_psych",
                  "FactValueNumeric_alcohol",
                  "HDI",
                  "Health_Expenditure", 
                  "HomicideRate"]

minmax_scaled[info_columns] = MinMaxScaler().fit_transform(combined_df[info_columns])

minmax_scaled.to_csv("complete_data_minmax.csv")

def plot_data(data, labels):
    # create combinations of columns
    combos = product(["HealthAvailVal_nurse",
                    "suicide_rate",
                    "HealthAvailVal_psych"], ["HealthAvailVal_nurse",
                    "suicide_rate",
                    "HealthAvailVal_psych"])
    combos = product(info_columns, ["suicide_rate"])

    # create subplots
    fig, axes = plt.subplots(nrows=len(data.columns)-2, ncols=1)

    # flatten axes into a 1d array
    axes = axes.flat

    # iterate and plot
    for (x, y), ax in zip(combos, axes):
        ax.scatter(data[x], data[y], c=labels)
        ax.set(title=f'{x} vs. {y}', xlabel=x, ylabel=y)
        # ax.set(xlabel=x, ylabel=y)
        # ax.set(title=f'{x} vs. {y}')
    plt.tight_layout()
    plt.show()

kmeans = []

for i in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
    kmeans.append(cl.KMeans(n_clusters=i))
    kmeans[-1].fit(minmax_scaled[info_columns])
    print("Davies Bouldin: " + str(dv.davies_bouldin_score(minmax_scaled[info_columns], kmeans[-1].labels_)))

plot_data(minmax_scaled, kmeans[0].labels_)
plot_data(minmax_scaled, kmeans[5].labels_)
plot_data(minmax_scaled, kmeans[9].labels_)

print(combined_df.head(10))
print(minmax_scaled.head(10))