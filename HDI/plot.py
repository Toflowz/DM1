import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

df = pd.read_csv('df_merged.csv')

years = df.Period.unique() # list of years

country_list = df.Location.unique() # list of countries

E_year_school = df[df['indicator'] == 'Expected Years of Schooling (years)']

print(E_year_school)
#for country in country_list:
#    temp = E_year_school[E_year_school['Location'] == country]
#    x = temp['value'].to_list()

#    suicide_rate = temp = E_year_school[E_year_school['Location'] == country]
#    y = suicide_rate['FactValueNumeric'].to_list()
#    if (len(x) == 20):
#        plt.scatter(x, y, c=years)
#        plt.xlabel('Expected Years of Schooling (years)')
#        plt.ylabel("Age-standardized suicide rate (per 100 000 population)")
#        plt.title("Scatter plot of x vs y for " + country + ", colors indicate year, lighter color is later year")
#        plt.show()

temp = E_year_school[E_year_school['Period'] == 2010]
print(temp)
x = temp['value'].to_list()

suicide_rate = temp = E_year_school[E_year_school['Period'] == 2010]
y = suicide_rate['FactValueNumeric'].to_list()

plt.scatter(x, y, c=temp.index)
plt.xlabel('Expected Years of Schooling')
plt.ylabel("Age-standardized suicide rate (per 100 000 population)")
plt.title("Scatter plot of x vs y for 2010, colors indicate country")
plt.show()
    #temp = E_year_school[E_year_school['Location'] == country]
    #y = temp['value'].to_list()

    #suicide_rate = temp = E_year_school[E_year_school['Location'] == country]
    #x = suicide_rate['FactValueNumeric'].to_list()

    #if (len(y) == 20):
        #plt.scatter(x, y)
        #plt.xlabel("X-axis")  # add X-axis label
        #plt.ylabel("Y-axis")  # add Y-axis label
        #plt.title("Any suitable title")  # add title
        #plt.show()

#M_year_school = df[df['indicator'] == 'Mean Years of Schooling (years)']
#GNI = df[df['indicator'] == 'Gross National Income Per Capita (2017 PPP$)']
#LE = df[df['indicator'] == 'Life Expectancy at Birth (years)']
#HDI = df[df['indicator'] == 'Human Development Index (value)']



#plt.xlabel("Year")
#plt.ylabel("Y-axis")  # add Y-axis label
#plt.title("Any suitable title")  # add title
#plt.show()