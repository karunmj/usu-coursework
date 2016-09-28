'''
CEE6110 assignment#2
Karun Joseph, A02240287

Purpose:
	Query Dark Sky API to obtain weather data
	Import SD card text file 
	Create plots between room, thermostat and external temperature
'''

#TODO: clean up report language
#TODO: take pictures, prepare building plan
#TODO: hit dark sky thursday morning to query wednesday data (midnight to 11pm)
#TODO: collect ardunio data from wednesday midnight to wednesday 11pm
#TODO: cleaner plots for time series and correlation

import json
import urllib2
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy import stats
import numpy as np

###Assembling necessary data

##External temperature
#epoch time for 9/27/16, 12:00am, gmt-6 (Mountain time)
epochtime = str(1475042400) 
#dark sky api end point to obtain hourly temperature data from 00:00 to 23:00 for 9/27/16, gmt-6 (Mountain time)
url = "https://api.darksky.net/forecast/28bbca577244c08e371c215bf3c75a5f/41.7352158,-111.8485149,"+epochtime
weather_data = json.load(urllib2.urlopen(url))
ext_hourly_temp = [x['temperature'] for x in weather_data['hourly']['data']]

##Internal thermostat temp
tempsetpoint = 70 #TODO: check for correct one
int_thermo_hourly_temp = [tempsetpoint]*len(ext_hourly_temp)

##Internal room temp
#Open SD card text file
temphumfile = pd.read_csv('HW1-1.TXT')
#int_room_hourly_temp = list(temphumfile['Temperature'])
int_room_hourly_temp = [65]*len(ext_hourly_temp) #TODO: uncomment above line when data available


###Plots

##Time series plot
plt.plot(temphumfile['ElapsedTime(us)'], temphumfile['Humidity'], 'g-', temphumfile['ElapsedTime(us)'], temphumfile['Temperature'], 'ro' )
plt.show()

##Scatterplot
#Pearsons coeffeciant
print "Pearsons correlation bw internal room temp and external temp: ", stats.pearsonr(int_room_hourly_temp,ext_hourly_temp)
plt.scatter(int_room_hourly_temp,ext_hourly_temp, c=np.random.rand(len(int_room_hourly_temp)))
plt.show()





