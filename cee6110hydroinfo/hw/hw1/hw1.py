##Plotting pH and dissolved oxygen levels
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#csv file contains logan river data for 2015 from water lab site
loganriverdata = pd.read_csv('iUTAH_GAMUT_LR_WaterLab_AA_RawData_2015.csv', skiprows=68)

#plotting ph
plt.plot(loganriverdata['pH'])
plt.ylabel('ph')
plt.xlabel('Time units [every 15 min]')
plt.title('pH levels, 2015')
plt.show()

#plotting dissolved oxygen
plt.plot(loganriverdata['ODO'])
plt.ylabel('Dissolved oxgen [mg/L]')
plt.xlabel('Time units [every 15 min]')
plt.title('Dissolved oxygen levels, 2015')
plt.show()





