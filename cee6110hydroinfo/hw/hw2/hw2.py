'''
CEE6110 assignment#2
Karun Joseph, A02240287

Python file for analysing SD card text file and plots for visualization
'''

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 

temphumfile = pd.read_csv('HW1-1.TXT')

plt.plot(temphumfile['ElapsedTime(us)'], temphumfile['Humidity'], 'g-', temphumfile['ElapsedTime(us)'], temphumfile['Temperature'], 'ro' )
plt.show()



