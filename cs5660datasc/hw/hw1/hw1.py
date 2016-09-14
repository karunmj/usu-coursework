"""
Questions
	0. Importing CSV best way. Each row as a dictionary, a panda dataframe?	
	1. Preprocessing - remove any building whose wu is ''?
	1. Best way to viz 1722 boxplots of all buildings? 
	1.1 Top 5 depts: in terms of number of buildings?
	1.2 Can we regard '0' as an extreme value (and ignore the same in 1.1)? Is there an upperbound(TODO: plot and see)?
"""

#Importing csv data 
import csv
#import pandas


#Plotting
import matplotlib.pyplot as plt
import numpy as np


with open('CAStateBuildingMetrics.csv', 'r') as csvfile:
	#Is this the best method? How about pandas data object?
	reader = csv.DictReader(csvfile)
	tcounter = 0

	for row in reader:
		#Water usage analysis
		tcounter+=1
		if row['Water Use (All Water Sources) (kgal)'] == '':
			print "NA"
		if row['Water Use (All Water Sources) (kgal)'] == '':
			print row['Property Id']
		# else:
		# 	print row['Water Use (All Water Sources) (kgal)']
	print tcounter	

# #Example code for plotting boxplots. Currenty matplotlob, numpy but later ggplot?
# spread = np.random.rand(50) * 100
# center = np.ones(25) * 50
# flier_high = np.random.rand(10) * 100 + 100
# flier_low = np.random.rand(10) * -100
# data = np.concatenate((spread, center, flier_high, flier_low), 0)

# # basic plot
# plt.boxplot(data)
# plt.show()



