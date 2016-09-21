"""
Questions - 9/14
	1. Best way to deal with NaN for water consumption: ignore / replace with mean of all water values/ others?
	2. What is the upperbound, lowerbound for water consumption? q1-q3?
TODO - 
	1. Ignoring outliers
	2. Q3
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csdf = pd.read_csv('CAStateBuildingMetrics.csv')

###############################
####1. Water usage analysis####
###############################

#Preprocessing - Replacing NaN with 0 / mean
#csdfclean = csdf['Water Use (All Water Sources) (kgal)'].dropna()
csdfclean = csdf['Water Use (All Water Sources) (kgal)'].fillna(csdf['Water Use (All Water Sources) (kgal)'].mean())

#Mean, Median, mode of all data
print "Mean with outliers", csdfclean.mean()
print "Median with outliers", csdfclean.median()
print "Mode with outliers", csdfclean.mode()

#List of top 5 departments in terms of number of buildings
uniquedept = dict()
for index, row in csdf.iterrows():
	if row['Department'] in uniquedept.keys():
		uniquedept[row['Department']]+=1
	else:
		uniquedept[row['Department']]=1 
top5dept = sorted(uniquedept.items(), key=lambda x:x[1], reverse = True)[0:5]

#Box plot for all buldings
plt.boxplot(csdfclean)
plt.show()

#Box plots for top 5 dept
csdf_top5=pd.DataFrame(columns=[dept[0] for dept in top5dept])

for index, row in csdf.iterrows():
	if row.Department in [dept[0] for dept in top5dept]:
		#Poor approach. Can be more efficient
		csdf_top5=csdf_top5.append({row['Department']:row['Water Use (All Water Sources) (kgal)']}, ignore_index=True)

plt.boxplot([csdf_top5['CAL TRANS'].dropna(), csdf_top5['CAL FIRE'].dropna(), csdf_top5['DPR'].dropna(), csdf_top5['CHP'].dropna(), csdf_top5['CMD'].dropna()])
plt.show()

#Ignoring outliers, preprocessing
q3=csdfclean.quantile(0.75)
q1=csdfclean.quantile(0.25)

# Mean, Median, mode of datawithout outiers
# print "Mean without outliers", csdfcleanno.mean()
# print "Median without outliers", csdfcleanno.median()
# print "Mode without outliers", csdfcleanno.mode()

#Box plots for all buldings without outliers
plt.boxplot(csdfclean,0,'') #not sure
plt.show()

#Box plots for top 5 departments without outliers
#TODO



#####################################
####2. Resource usage correlation####
#####################################

#Scatter plot between electricity and water usage
#TODO: how does plot deal with NaN values
plt.scatter(csdf['Water Use (All Water Sources) (kgal)'], csdf['Electricity Use (kWh)'], c=np.random.rand(len(csdf.index)))
plt.show()

#Persons correlation
print "Persons correlation bw electricitiy and water usage ", csdf[['Water Use (All Water Sources) (kgal)', 'Electricity Use (kWh)']].corr(method='pearson')

#For the top five dept
#TODO



# ################################
# ####3. Building similarities####
# ################################

#List of attributes
list(csdf.columns.values)

#Slice of row whose property name matches query
mendota_main_st = csdf.loc[csdf['Property Name']=='MENDOTA MAINTENANCE STATION']
metro_state_hosp = csdf.loc[csdf['Property Name']=='METROPOLITAN STATE HOSPITAL']
long_beach_foffice = csdf.loc[csdf['Property Name']=='LONG BEACH FIELD OFFICE']

#Variabes of interest include 
#Resource usage: electricity use, natural gas use, propane use, water use, site energy use
#Property variables: dept name, city, primary property type, area
#Both together

