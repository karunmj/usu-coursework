"""
Questions

TODO - 
	2. Q3
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial
import statistics

csdf = pd.read_csv('CAStateBuildingMetrics.csv')

###############################
####1. Water usage analysis####
###############################

#Preprocessing - Replacing NaN with 0 / mean
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

#Ignoring outliers, preprocessing with upper limit = q3 + (1.5*qir), lower limit = q1 - (1.5*qir)
q3=csdfclean.quantile(0.75)
q1=csdfclean.quantile(0.25)

# Mean, Median, mode of datawithout outiers
print "Mean without outliers", statistics.mean([x for x in csdfclean if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])
print "Median without outliers", statistics.median([x for x in csdfclean if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])
print "Mode without outliers", statistics.mode([x for x in csdfclean if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])



#####################################
####2. Resource usage correlation####
#####################################

#Scatter plot between electricity and water usage TODO: how does plot deal with NaN values
plt.scatter(csdf['Water Use (All Water Sources) (kgal)'], csdf['Electricity Use (kWh)'], c=np.random.rand(len(csdf.index)))
plt.show()

#Persons correlation
print "Persons correlation bw electricitiy and water usage ", csdf[['Water Use (All Water Sources) (kgal)', 'Electricity Use (kWh)']].corr(method='pearson')

#For the top five dept
#TODO



# ################################
# ####3. Building similarities####
# ################################

# Similarities: Euclidian, Manahattan, Cosine
# Variabes of interest include 
# 	Resource usage: electricity use(kwh), natural gas use(therms), propane use(kbtu), water use(kgal), site energy use (kbtu)
# 	Property variables: dept name, city, primary property type, area
# 	Both together

#List of attributes
list(csdf.columns.values)

#Slice of row whose property name matches query
mendota_main_st = csdf.loc[csdf['Property Name']=='MENDOTA MAINTENANCE STATION']
metro_state_hosp = csdf.loc[csdf['Property Name']=='METROPOLITAN STATE HOSPITAL']
long_beach_foffice = csdf.loc[csdf['Property Name']=='LONG BEACH FIELD OFFICE']

