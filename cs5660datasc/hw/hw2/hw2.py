'''
questions:
	locations outside US and Canada? For pre processing exclude them by: if state field is empty?
	deal with duration? For just first 100 records (~/10812), there are 'Still happening', '22:00', 'few minutes', 'several minutes', 'brief', '~1 hour', 'route 6', 'north close to the firing', 'Few seconds'
	bar chart of sightings per state: is it cir, tr, fire summed or separate?

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle 
import datetime
from dateutil import parser
import json
import numpy as np

###data collection, pre processing, exploratory analysis

##circle, triangle, fireball data scraping, pickling
'''
#data scraping
circle_url = 'http://www.nuforc.org/webreports/ndxsCircle.html'
circle_req = requests.get(circle_url)
circle_soup = BeautifulSoup(circle_req.text,'html.parser')

triangle_url = 'http://www.nuforc.org/webreports/ndxsTriangle.html'
triangle_req = requests.get(triangle_url)
triangle_soup = BeautifulSoup(triangle_req.text,'html.parser')

fireball_url = 'http://www.nuforc.org/webreports/ndxsFireball.html'
fireball_req = requests.get(fireball_url)
fireball_soup = BeautifulSoup(fireball_req.text,'html.parser')

#data timeframe formatting
circle_column_headers = [x.getText() for x in circle_soup.findAll('tr', limit=1)[0].findAll('th')]
circle_tr_rows = circle_soup.findAll('tr')[1:]
circle_table = [[x.getText() for x in row.findAll('td')] for row in circle_tr_rows]
circle_df = pd.DataFrame(circle_table, columns=circle_column_headers)

triangle_column_headers = [x.getText() for x in triangle_soup.findAll('tr', limit=1)[0].findAll('th')]
triangle_tr_rows = triangle_soup.findAll('tr')[1:]
triangle_table = [[x.getText() for x in row.findAll('td')] for row in triangle_tr_rows]
triangle_df = pd.DataFrame(triangle_table, columns=triangle_column_headers)

fireball_column_headers = [x.getText() for x in fireball_soup.findAll('tr', limit=1)[0].findAll('th')]
fireball_tr_rows = fireball_soup.findAll('tr')[1:]
fireball_table = [[x.getText() for x in row.findAll('td')] for row in fireball_tr_rows]
fireball_df = pd.DataFrame(fireball_table, columns=fireball_column_headers)

pickle.dump(circle_df, open("circle_df.p", "wb"))
pickle.dump(triangle_df, open("triangle_df.p", "wb"))
pickle.dump(fireball_df, open("fireball_df.p", "wb"))

#circle_df = pickle.load(open("circle_df.p", "rb"))
#triangle_df = pickle.load(open("triangle_df.p", "rb"))
#fireball_df = pickle.load(open("fireball_df.p", "rb"))

#combine circle, triangle, fireball dataframe
#allshape_df = circle_df.append([triangle_df, fireball_df], ignore_index=True)

#(slow and ugly, may need alt)
#preprocessing - include sightings only bw 1/1/2005 and 9/22/2016. New column 'in_range' will be set to 1 if true
allshape_df['in range'] = [0]*len(allshape_df.index)
for index, row in allshape_df.iterrows():
    try:
        datetimesighting = parser.parse(row['Date / Time'])
        if datetime.datetime(2005, 1, 1) <= datetimesighting <= datetime.datetime(2015, 9, 22):
            allshape_df.set_value(index,'in range', 1)
        else:
            continue
    except:
    	pass

pickle.dump(allshape_df, open("allshape_df.p", "wb"))
'''

#loading datarame that has combined circle, traingle and fireball data
allshape_df = pickle.load(open("allshape_df.p", "rb"))
#newdata frame to hold in range duration rows only
allshape_inrange_df=(pd.DataFrame([row for index, row in allshape_df.iterrows() if row['in range']==1])).reset_index(drop=True)
#creating new column with datetime objects
allshape_inrange_df['datetime'] =pd.to_datetime(allshape_inrange_df['Date / Time'])
#sorting dataframe by datetime column
allshape_inrange_df = (allshape_inrange_df.sort_values('datetime')).reset_index(drop=True)

##preprocessing - nicer format 'duration', 'duration' to seconds
#TODO

##preprocessing - take out outside us locations, create region column
stateregion = json.load(open('stateregion.json'))

allshape_inrange_us_df = pd.DataFrame(columns=list(allshape_inrange_df.columns.values))
for index, row in allshape_inrange_df.iterrows():
    if row.State in [stateid for stateid in stateregion['states']]:
        allshape_inrange_us_df=allshape_inrange_us_df.append(row, ignore_index=True)

region = []
for index, row in allshape_inrange_us_df.iterrows():
    #allshape_inrange_us_df.iloc[index,10] = stateregion['states'][allshape_inrange_us_df.iloc[index]['State']]
    region.append(stateregion['states'][row.State])
allshape_inrange_us_df['region']=region

##box plot of duration

##time series plot of number of sightings

##bar chart of sightings

##normalizing by state population
#Population data from US census
population_api = requests.get('http://api.census.gov/data/2015/acs1/cprofile?get=CP05_2015_001E,NAME&for=state:*')
population = population_api.text

###predicting ufo shape
##preprocessing - time to n, m, af, ev
