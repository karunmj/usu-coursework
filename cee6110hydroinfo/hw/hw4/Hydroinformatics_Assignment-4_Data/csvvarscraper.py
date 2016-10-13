#Preprcoess GAMUT file to return ph and specific conductance csv files.
#

import pandas as pd 

loganriver = pd.read_csv('iUTAH_GAMUT_LR_MainStreet_BA_RawData_2014.csv', skiprows = 57, index_col=False)

##ph
ph = loganriver[[' pH', 'LocalDateTime', ' UTCOffset', ' DateTimeUTC']]

siteid = [2] * len(loganriver.index)
variableid = [3] * len(loganriver.index)
methodid = [8] * len(loganriver.index)
sourceid = [1] * len(loganriver.index)
qualitycontrollevelid = [0] * len(loganriver.index)

ph['SiteID'] = siteid
ph['VariableID'] = variableid
ph['MethodID'] = methodid
ph['SourceID'] = sourceid
ph['QualityControlLevelID'] = qualitycontrollevelid 

ph.rename(columns={' pH': 'DataValue', ' UTCOffset': 'UTCOffset', ' DateTimeUTC': 'DateTimeUTC'}, inplace=True)

gooddatetimeutc = []
[gooddatetimeutc.append(row['DateTimeUTC'].lstrip()) for index, row in ph.iterrows()]
ph = ph.assign(DateTimeUTC = gooddatetimeutc)

ph.to_csv('ph.csv', index=False)


##sp
sp = loganriver[[' SpCond', 'LocalDateTime', ' UTCOffset', ' DateTimeUTC']]

siteid = [2] * len(loganriver.index)
variableid = [2] * len(loganriver.index)
methodid = [7] * len(loganriver.index)
sourceid = [1] * len(loganriver.index)
qualitycontrollevelid = [0] * len(loganriver.index)

sp['SiteID'] = siteid
sp['VariableID'] = variableid
sp['MethodID'] = methodid
sp['SourceID'] = sourceid
sp['QualityControlLevelID'] = qualitycontrollevelid 

sp.rename(columns={' SpCond': 'DataValue', ' UTCOffset': 'UTCOffset', ' DateTimeUTC': 'DateTimeUTC'}, inplace=True)

gooddatetimeutc = []
[gooddatetimeutc.append(row['DateTimeUTC'].lstrip()) for index, row in ph.iterrows()]
sp = sp.assign(DateTimeUTC = gooddatetimeutc)

sp.to_csv('sp.csv', index=False)


##usgs gauge data
logandaily = pd.read_csv('LoganDailyflow.csv')
logandailyflow = logandaily[['agency_cd', 'site_no', 'Date', 'X_00060_00003']]

#TODO:
# siteid = [] * len(logandailyflow.index) #new site id
# variableid = [] * len(logandailyflow.index) #insert variable id for usgs flow
# methodid = [26] * len(logandailyflow.index) 
# sourceid = [2] * len(logandailyflow.index) 
# qualitycontrollevelid = [0] * len(logandailyflow.index)

