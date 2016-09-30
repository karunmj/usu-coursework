'''
questions:
	sightings only till 9/21/2016 (inlcuding)
	locations outside US and Canada? For pre processing exclude them by: if state field is empty?
	deal with duration? For just first 100 records (~/10812), there are 'Still happening', '22:00', 'few minutes', 'several minutes', 'brief', '~1 hour', 'route 6', 'north close to the firing', 'Few seconds'
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle 


###data collection, pre processing, exploratory analysis

##circles##


'''
#data scraping
circle_url = 'http://www.nuforc.org/webreports/ndxsCircle.html'
circle_req = requests.get(circle_url)
circle_soup = BeautifulSoup(circle_r.text)

#data timeframe formatting
circle_column_headers = [x.getText() for x in circle_soup.findAll('tr', limit=1)[0].findAll('th')]
circle_tr_rows = circle_soup.findAll('tr')[1:]
circle_table = [[x.getText() for x in row.findAll('td')] for row in circle_tr_rows]
circle_df = pd.DataFrame(circle_table, columns=circle_column_headers)
pickle.dump(circle_df, open("circle_df.p", "wb"))

'''

circle_df = pickle.load(open("circle_df.p", "rb"))
print circle_df.head()

#TODO: split 'Date/ Time' column to 2 columns 'Date' and 'Time'

#preprocessing - inlcude sightings only bw 1/1/2005 and 9/22/2016

#preprocessing - nicer format 'duration', 'duration' to seconds


#Population data from US census
population_api = requests.get('http://api.census.gov/data/2015/acs1/cprofile?get=CP05_2015_001E,NAME&for=state:*')
population = population_api.text
print population


