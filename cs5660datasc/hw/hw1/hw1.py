"""
Questions - 9/14
	1. Best way to deal with NaN for water consumption: ignore / replace with mean of all water values/ others?
	2. What is the upperbound for water consumption?
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csdf = pd.read_csv('CAStateBuildingMetrics.csv')

###############################
####1. Water usage analysis####
###############################

#Preprocessing - ignoring NaN values. Mostly incorrect, may have to replace NaN with the mean?
csdfclean = csdf['Water Use (All Water Sources) (kgal)'].dropna()

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
#csdf_top5=pd.DataFrame(columns=[dept[0] for dept in top5dept])
csdf_top5=[]

for index, row in csdf.iterrows():
	if row.Department in [dept[0] for dept in top5dept]:
		print "top 5 building!"
		print dept[0]
		#TODO: how to store above info for plotting? Tried data frame with 5 columns, after each loop add. Now trying tuples in a list
		#csdf_top5.append({'DPR':6}, ignore_index=True)

	else:
		print "not a top5 building!"
		
# plt.figure()
# plt.boxplot(csdf_top5)
# plt.show()

#Ignoring outliers, preprocessing
# TODO: csdfcleanno

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



