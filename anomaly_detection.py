from pyod.models.knn import KNN
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
from pyod.utils.example import visualize
import pandas as pd
from sklearn.ensemble import IsolationForest
from itertools import product
import matplotlib.pyplot as plt
# from combined_data import plot_data

basic_df = pd.read_csv("complete_data.csv")
df = pd.read_csv("complete_data_minmax.csv")
info_columns = ["HealthAvailVal_nurse",
                  "suicide_rate",
                  "HealthAvailVal_psych",
                  "FactValueNumeric_alcohol",
                  "HDI",
                  "Health_Expenditure", 
                  "HomicideRate"]
country = pd.read_csv("Mental Health Availability/codes/COUNTRY.csv")

# #Create a model
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


clf = IsolationForest()
clf.fit(df[info_columns])
anomaly_score = clf.predict(df[info_columns])

# print(anomaly_score)
for i in range(0,len(anomaly_score)):
    if anomaly_score[i] == -1:
        # anomlay detect
        country_code = df.iat[i,1]
        print("Country with anomaluos data is: " + str(country.loc[country["Code"] == country_code, "Title"].item()))
        print(basic_df[basic_df["SpatialDimValueCode"] == country_code])


plot_data(df, anomaly_score)
# #Test trained model
#  y_test_scores = clf.decision_function(X_test) #outlier scores
# y_train_pred = clf.predict(X_train)
# y_test_pred = clf.predict(X_test) #Outlier labels (0 or 1)


#Reporting performance
#print(f"IsolationForest roc_auc_score: {roc_auc_score(y_test, y_test_scores)}")
#print(f"IsolationForest average_precision_score: {average_precision_score(y_test, y_test_scores)}")