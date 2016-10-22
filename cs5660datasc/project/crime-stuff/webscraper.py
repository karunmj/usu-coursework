
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

'''
##Trying to get thos script run for any paramters

payload = {'StateID': '45', 'DataType': '1', 'DataType': '2', 'DataType': '3', 'DataType': '4', 'YearStart': '1961', 'NextPage': 'Get Table'}
r = requests.get('http://149.101.16.41:80/', params=payload)
print r.url
soup = BeautifulSoup(r.text,'html.parser')
print soup.prettify()
'''

## The footer section doesn't work. Might want to do some excel type formatting, or ignore 
utah_data = pd.read_csv('CrimeStatebyUT.csv', skiprows = 5, )#, skipfooter = 6)
us_2012_data = pd.read_csv('CrimeOneYearofData2012.csv', skiprows = 6) #skipfooter = 62)



