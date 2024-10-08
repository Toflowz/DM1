import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def enumerateCol(data):
    enum = enumerate(data)
    return [x[0] for x in enum]

def plotScatter(data):
    data = data[data["Dim1"] == "Both sexes"]
    plt.title("")
    plt.scatter(data["Value_x"], data["FactValueNumeric"], c=enumerateCol(data["Location"]))
    plt.xlabel(data.DataName.unique()[0])
    plt.ylabel(data.Indicator.unique()[0])
    plt.show()

df = pd.read_csv("suicide_data.csv", delimiter = ",")
countries = pd.read_csv("Mental Health Availability/codes/COUNTRY.csv")
countries = countries.drop(columns = ["Dimension","ParentDimension","ParentCode","ParentTitle"])
GHO = pd.read_csv("Mental Health Availability/codes/GHO.csv")

data = np.empty(15, dtype=pd.DataFrame)

index = 0
for i in [6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 24]:
    data[index] = pd.read_csv(f"Mental Health Availability/data/MH_{i}.csv")
    index += 1

def create_db(data, countries, GHO):
    data = data[["IndicatorCode", "SpatialDimensionValueCode", "TimeDim", "Value", "NumericValue"]]
    data = data.merge(GHO, left_on="IndicatorCode", right_on="Code").drop(columns = ["Dimension", "IndicatorCode", "Code", "ParentDimension", "ParentCode", "ParentTitle"])
    data = data.merge(countries, left_on="SpatialDimensionValueCode", right_on="Code").drop(columns = ["Code"])
    data = data.rename(columns = {"SpatialDimensionValueCode": "CountryCode", "Title_x": "DataName", "Title_y": "Country"})
    data = data.merge(df, left_on=["CountryCode", "TimeDim"], right_on=["SpatialDimValueCode", "Period"])
    data = data[data["Dim1"] == "Both sexes"]
    data = data.drop(columns = ["FactValueNumericHighPrefix", 
                                      "FactValueTranslationID", 
                                      "FactComments", 
                                      "Language", 
                                      "FactValueUoM", 
                                      "FactValueNumericLowPrefix",
                                      "DataSource", 
                                      "FactValueNumericPrefix",
                                      "Dim3ValueCode", 
                                      "DataSourceDimValueCode",
                                      "IndicatorCode",
                                      "Dim3 type", 
                                      "Dim3",
                                      "Dim2", 
                                      "Dim2ValueCode",
                                      "Dim2 type",
                                      "Dim1ValueCode",
                                      "Dim1 type",
                                      "DateModified",
                                      "IsLatestYear",
                                      "Period type",
                                      "TimeDim",
                                      "ValueType",
                                      "ParentLocationCode",
                                      "ParentLocation",
                                      "ParentLocationCode",
                                      "SpatialDimValueCode",
                                      "Location type",
                                      "NumericValue",
                                      "Country",
                                      "Location",
                                      "FactValueNumericLow",
                                      "FactValueNumericHigh",
                                      "Value_y",
                                      "DataName",
                                      "Indicator",
                                      "Dim1"])
    data = data.rename(columns = {"Value_x": "HealthAvailVal"})
    return data

create_db(data[0], countries, GHO).to_csv("Mental Health Availability/data/psychiatrists.csv")
create_db(data[1], countries, GHO).to_csv("Mental Health Availability/data/nurses.csv")

for i in range(15):
    data[i] = create_db(data[i], countries=countries, GHO=GHO)
    print(data[i].Period.unique())