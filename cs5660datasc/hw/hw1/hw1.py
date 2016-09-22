#TODO: nicer plots, scatteplots for top5
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial, stats
import statistics

csdf = pd.read_csv('CAStateBuildingMetrics.csv')

###############################
####1. Water usage analysis####
###############################
#Preprocessing - Replacing NaN with 0 / mean
csdf_clean_water= csdf[['Water Use (All Water Sources) (kgal)', 'Department']].fillna(csdf['Water Use (All Water Sources) (kgal)'].mean())

##Mean, Median, mode of all data
print "Mean with outliers", csdf_clean_water.mean()
print "Median with outliers", csdf_clean_water.median()
print "Mode with outliers", csdf_clean_water.mode()

#List of top 5 departments in terms of number of buildings
uniquedept = dict()
for index, row in csdf.iterrows():
	if row['Department'] in uniquedept.keys():
		uniquedept[row['Department']]+=1
	else:
		uniquedept[row['Department']]=1 
top5dept = sorted(uniquedept.items(), key=lambda x:x[1], reverse = True)[0:5]
	
##Box plot for all buldings
plt.boxplot(csdf_clean_water['Water Use (All Water Sources) (kgal)'])
plt.show()
#Without outliers, zoomed in
plt.boxplot(csdf_clean_water['Water Use (All Water Sources) (kgal)'],0,'') 
plt.show()

##Box plots for top 5 dept
csdf_top5_water=pd.DataFrame(columns=[dept[0] for dept in top5dept])
for index, row in csdf_clean_water.iterrows():
	if row.Department in [dept[0] for dept in top5dept]:
		csdf_top5_water=csdf_top5_water.append({row['Department']:row['Water Use (All Water Sources) (kgal)']}, ignore_index=True)

plt.boxplot([csdf_top5_water['CAL TRANS'].dropna(), csdf_top5_water['CAL FIRE'].dropna(), csdf_top5_water['DPR'].dropna(), csdf_top5_water['CHP'].dropna(), csdf_top5_water['CMD'].dropna()])
plt.show()

#Ignoring outliers, preprocessing with upper limit = q3 + (1.5*qir), lower limit = q1 - (1.5*qir)
q3=csdf_clean_water['Water Use (All Water Sources) (kgal)'].quantile(0.75)
q1=csdf_clean_water['Water Use (All Water Sources) (kgal)'].quantile(0.25)

## Mean, Median, mode of data without outiers
print "Mean without outliers", statistics.mean([x for x in csdf_clean_water['Water Use (All Water Sources) (kgal)'] if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])
print "Median without outliers", statistics.median([x for x in csdf_clean_water['Water Use (All Water Sources) (kgal)'] if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])
print "Mode without outliers", statistics.mode([x for x in csdf_clean_water['Water Use (All Water Sources) (kgal)'] if x>(q1-1.5*(q3-q1)) and x<(q3+1.5*(q3-q1))])



#####################################
####2. Resource usage correlation####
#####################################
csdf_clean_elec = csdf[['Electricity Use (kWh)', 'Department']].fillna(csdf['Electricity Use (kWh)'].mean())

##Scatter plot between electricity and water usage
plt.scatter(csdf_clean_water['Water Use (All Water Sources) (kgal)'], csdf_clean_elec['Electricity Use (kWh)'], c=np.random.rand(len(csdf.index)))
plt.show()

##Persons correlation
print "Persons correlation bw electricitiy and water usage ", stats.pearsonr(csdf_clean_water['Water Use (All Water Sources) (kgal)'], csdf_clean_elec['Electricity Use (kWh)'])


#For the top five dept
csdf_top5_elec=pd.DataFrame(columns=[dept[0] for dept in top5dept])
for index, row in csdf_clean_elec.iterrows():
	if row.Department in [dept[0] for dept in top5dept]:
		csdf_top5_elec=csdf_top5_elec.append({row['Department']:row['Electricity Use (kWh)']}, ignore_index=True)

#TODO: Not working
# plt.scatter(csdf_top5_water['CAL TRANS'], csdf_top5_elec['CAL TRANS'], c=np.random.rand(len(csdf_top5_water.index)))
# plt.show()
# print "Persons correlation bw electricitiy and water usage for CAL TRANS", stats.pearsonr(csdf_top5_water['CAL TRANS'], csdf_top5_elec['CAL TRANS'])

# plt.scatter(csdf_top5_water['CAL FIRE'], csdf_top5_elec['CAL FIRE'], c=np.random.rand(len(csdf_top5_water.index)))
# plt.show()
# print "Persons correlation bw electricitiy and water usage for CAL FIRE", stats.pearsonr(csdf_top5_water['CAL FIRE'], csdf_top5_elec['CAL FIRE'])


# ################################
# ####3. Building similarities####
# ################################
#helpful checks = list(csdf.columns.values); [x for x in cities.isnull() if x==True]

##Electricity, natural gas, propane, water, site energy use
csdf_clean_elec=csdf[['Property Name', 'Electricity Use (kWh)']].fillna(csdf['Electricity Use (kWh)'].mean())
csdf_clean_water=csdf['Water Use (All Water Sources) (kgal)'].fillna(csdf['Water Use (All Water Sources) (kgal)'].mean())
csdf_clean_naturalgas = csdf['Natural Gas Use (therms)'].fillna(csdf['Natural Gas Use (therms)'].mean())
csdf_clean_propane = csdf['Propane Use (kBtu)'].fillna(csdf['Propane Use (kBtu)'].mean())
csdf_clean_siteenergy=csdf['Site Energy Use (kBtu)'].fillna(csdf['Site Energy Use (kBtu)'].mean())

#Combine all clean usage data into one df
csdf_clean_totalresusage=pd.concat([csdf_clean_elec, csdf_clean_water, csdf_clean_naturalgas, csdf_clean_propane, csdf_clean_siteenergy], axis=1)

#Slice of row whose property name matches query
mendota_main_st = csdf_clean_totalresusage.loc[csdf['Property Name']=='MENDOTA MAINTENANCE STATION']
metro_state_hosp = csdf_clean_totalresusage.loc[csdf['Property Name']=='METROPOLITAN STATE HOSPITAL']
long_beach_foffice = csdf_clean_totalresusage.loc[csdf['Property Name']=='LONG BEACH FIELD OFFICE']

#Mendota
print "Mendota res cosine ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Mendota res euclidian ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Mendota res manhattan ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 

#Metro
print "Metro res cosine ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Metro res euclidian ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Metro res manhattan ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 

#Long beach
print "Long beach res cosine ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Long beach res euclidian ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 
print "Long beach res manhattan ", csdf_clean_totalresusage.ix[[x[1] for x in sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_totalresusage.ix[:,1:].iterrows()])[0:4] 

##Department name, city, primary property type, property area
#Preprocessing involves regarding cities of any case(L/U) with same text as same. They are then converted to quant type by just assigning an integer to every unique city
csdf_clean_proparea=csdf[['Property Name', 'Property Area(ft\xc2\xb2)']].fillna(csdf['Property Area(ft\xc2\xb2)'].mean())

cities=csdf.City
uniquecities=list(set(cities.str.lower())) 
uniquecitiesdict = {row:index for index,row in enumerate(uniquecities)}
csdf_clean_city = pd.DataFrame({'cities':[uniquecitiesdict[row.lower()] for index,row in cities.iteritems()]})

deptnames=csdf.Department
uniquedeptnames=list(set(deptnames.str.lower())) 
uniquedeptnamesdict = {row:index for index,row in enumerate(uniquedeptnames)}
csdf_clean_deptname = pd.DataFrame({'deptnames':[uniquedeptnamesdict[row.lower()] for index,row in deptnames.iteritems()]})

proptype=csdf['Primary Property Type ']
uniqueproptype=list(set(proptype.str.lower())) 
uniqueproptypedict = {row:index for index,row in enumerate(uniqueproptype)}
csdf_clean_proptype = pd.DataFrame({'proptype':[uniqueproptypedict[row.lower()] for index,row in proptype.iteritems()]})

csdf_clean_propvar = pd.concat([csdf_clean_proparea, csdf_clean_deptname, csdf_clean_city, csdf_clean_proptype], axis=1)

mendota_main_st = csdf_clean_propvar.loc[csdf['Property Name']=='MENDOTA MAINTENANCE STATION']
metro_state_hosp = csdf_clean_propvar.loc[csdf['Property Name']=='METROPOLITAN STATE HOSPITAL']
long_beach_foffice = csdf_clean_propvar.loc[csdf['Property Name']=='LONG BEACH FIELD OFFICE']

#Mendota
print "Mendota res cosine ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Mendota res euclidian ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Mendota res manhattan ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 

#Metro
print "Metro res cosine ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Metro res euclidian ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Metro res manhattan ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 

#Long beach
print "Long beach res cosine ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Long beach res euclidian ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 
print "Long beach res manhattan ", csdf_clean_propvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_propvar.ix[:,1:].iterrows()])[0:4] 



#Electricity, natural gas, propane, water, site energy use, Department name, city, primary property type, property area

csdf_clean_proparea=csdf['Property Area(ft\xc2\xb2)'].fillna(csdf['Property Area(ft\xc2\xb2)'].mean())

csdf_clean_combvar = pd.concat([csdf_clean_elec, csdf_clean_water, csdf_clean_naturalgas, csdf_clean_propane, csdf_clean_siteenergy, csdf_clean_proparea, csdf_clean_deptname, csdf_clean_city, csdf_clean_proptype], axis=1)

mendota_main_st = csdf_clean_combvar.loc[csdf['Property Name']=='MENDOTA MAINTENANCE STATION']
metro_state_hosp = csdf_clean_combvar.loc[csdf['Property Name']=='METROPOLITAN STATE HOSPITAL']
long_beach_foffice = csdf_clean_combvar.loc[csdf['Property Name']=='LONG BEACH FIELD OFFICE']

#Mendota
print "Mendota res cosine ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Mendota res euclidian ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Mendota res manhattan ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(mendota_main_st.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 

#Metro
print "Metro res cosine ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Metro res euclidian ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Metro res manhattan ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(metro_state_hosp.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 

#Long beach
print "Long beach res cosine ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cosine(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Long beach res euclidian ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.euclidean(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
print "Long beach res manhattan ", csdf_clean_combvar.ix[[x[1] for x in sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4]],0], " : ",sorted([[spatial.distance.cityblock(long_beach_foffice.ix[:,1:],row),index] for index,row in csdf_clean_combvar.ix[:,1:].iterrows()])[0:4] 
