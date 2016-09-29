'''
CEE6110 assignment#2
Karun Joseph, A02240287

Purpose:
	Import SD card text file 
	Create plots between room and thermostat set point
'''

import pandas as pd 
import matplotlib.pyplot as plt 
from scipy import stats
import numpy as np


##Internal room temp
temp_df = pd.read_csv('HW1-3.TXT')
temp_df['hrindex'] = temp_df['ElapsedTime(us)']/(60*60)

##Internal thermostat temp
thermosetpoint = (76.0- 32) * 5/9
int_thermo_temp = [thermosetpoint]*len(temp_df.index)
temp_df['thermo_sp'] = int_thermo_temp

hour_format = [x for x in temp_df['hrindex']]

print "Mean with outliers", temp_df['Temperature'].mean()
print "Median with outliers", temp_df['Temperature'].median()
print "Mode with outliers", temp_df['Temperature'].mode()
print "q3", temp_df['Temperature'].quantile(0.75)
print "q1", temp_df['Temperature'].quantile(0.25)


#Time series plots
plt.plot(temp_df['hrindex'], temp_df['Temperature'], '-', label = "Room temperature")
plt.plot(temp_df['hrindex'], temp_df['thermo_sp'], 'r-', label = "Thermostat setpoint") 
plt.legend(loc='upper right')
plt.ylabel('Temperature (degC)')
plt.xlabel('Time (hours)')
plt.show()

#Box plot
plt.title('Box plot of room temperature')
plt.ylabel('Temperature (degC)')
plt.boxplot(temp_df['Temperature'],labels=['Room temperature'])
plt.show()




