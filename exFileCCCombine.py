from tokenize import String
import pandas as pd
import numpy as np

filePath = 'C:/Users/access/file1.csv'
df1 = pd.read_csv(filePath, dtype={'Solar Radiation-Pyranometer ': 'string', 'PAR': 'string'})

filePath = 'C:/Users/access/file2.csv'
df2 = pd.read_csv(filePath)

df2 = df2.drop(columns=['Notes'])
sorted_columns = sorted(df1.columns.tolist())
df1 = df1[sorted_columns]

sorted_columns2 = sorted(df2.columns.tolist())
df2 = df2[sorted_columns2]

df1.info()
df2.info()

df1.columns = ['Bar_Press', 'Air_Temp', 'Batt', 'GMT400', 'DewPt', 'Gust_Speed', 'PAR', 'Rain', 'RH', 'Moist60',
               'Temp20',  'Temp5', 'Temp60', 'Moist20', 'Moist5', 'Solar_Rad', 'Station', 'Wind_Dir', 'Wind_Speed']
df2.columns = ['Batt', 'GMT400', 'DewPt', 'Gust_Speed', 'PAR', 'Bar_Press', 'RH', 'Rain', 'Solar_Rad', 'Station',
               'Temp5', 'Temp20', 'Temp60', 'Air_Temp', 'Moist20', 'Moist5', 'Moist60', 'Wind_Dir', 'Wind_Speed']

sorted_columns = sorted(df1.columns.tolist())
df1 = df1[sorted_columns]

sorted_columns2 = sorted(df2.columns.tolist())
df2 = df2[sorted_columns2]

df1['GMT400'] = pd.to_datetime(df1['GMT400'])
df2['GMT400'] = pd.to_datetime(df2['GMT400'])

df1.info()
df2.info()

df1['PAR'] = df1['PAR'].str.replace(',', '', regex=False)
df1['PAR'] = pd.to_numeric(df1['PAR'])

df1['Solar_Rad'] = df1['Solar_Rad'].str.replace(',', '', regex=False)
df1['Solar_Rad'] = pd.to_numeric(df1['Solar_Rad'])

df1.info()
df2.info()
#%%
df = pd.concat([df1, df2])
df.info()
#%%
df1['Bar_Press'] = df1['Bar_Press'].astype('string')

soilFinal = df1[['GMT400', 'Station', 'Temp5', 'Temp20', 'Temp60', 'Moist20', 'Moist5', 'Moist60']]
sorted_columns = sorted(soilFinal.columns.tolist())
soilFinal = soilFinal[sorted_columns]
print(soilFinal.head())

finalDF = df1[['Bar_Press', 'Air_Temp', 'GMT400', 'DewPt', 'Gust_Speed', 'PAR', 'Rain', 'RH', 'Solar_Rad', 'Station', 'Wind_Dir', 'Wind_Speed', 'Batt']]
sorted_columns= sorted(finalDF.columns.tolist())
finalDF = finalDF[sorted_columns]
print(finalDF.head())

finalDF.to_csv('C:/Users/access/newCleanerOrganizedFile1.csv', index=False)
soilFinal.to_csv('C:/Users/access/newCleanerOrganizedFile2.csv', index=False)
#%%
