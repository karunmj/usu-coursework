'''
questions:
	sightings only till 9/21/2016 (inlcuding)
	locations outside US and Canada? For pre processing exclude them by: if state field is empty?
	deal with duration? For just first 100 records (~/10812), there are 'Still happening', '22:00', 'few minutes', 'several minutes', 'brief', '~1 hour', 'route 6', 'north close to the firing', 'Few seconds'
	bar chart of sightings per state: is it cir, tr, fire summed or separate?

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle 
import datetime
import parser

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
'''

circle_df = pickle.load(open("circle_df.p", "rb"))
triangle_df = pickle.load(open("triangle_df.p", "rb"))
fireball_df = pickle.load(open("fireball_df.p", "rb"))

#preprocessing: split 'Date/ Time' column to 2 columns 'Date' and 'Time'
def datetimesplitter(datetimeentry):
	#Function to split date and time. Some don't have time of sighting, seting them to '00:00'
	dateentry = datetimeentry[0] 
	if len(datetimeentry) > 1: 
		timeentry = datetimeentry[1]
	else:
		timeentry = '00:00'
	return [dateentry, timeentry]

circle_date_sighting = []
circle_time_sighting = []

triangle_date_sighting = []
triangle_time_sighting = []

fireball_date_sighting = []
fireball_time_sighting = []

circle_date_sighting,circle_time_sighting=zip(*[(x[0], x[1]) for x in [datetimesplitter(x.split(" ")) for x in circle_df['Date / Time']]])
circle_df['Date of sighting'] = circle_date_sighting
circle_df['Time of sighting'] = circle_time_sighting

triangle_date_sighting,triangle_time_sighting=zip(*[(x[0], x[1]) for x in [datetimesplitter(x.split(" ")) for x in triangle_df['Date / Time']]])
triangle_df['Date of sighting'] = triangle_date_sighting
triangle_df['Time of sighting'] = triangle_time_sighting

fireball_date_sighting,fireball_time_sighting=zip(*[(x[0], x[1]) for x in [datetimesplitter(x.split(" ")) for x in fireball_df['Date / Time']]])
fireball_df['Date of sighting'] = fireball_date_sighting
fireball_df['Time of sighting'] = fireball_time_sighting

# print circle_df.head()
# print triangle_df.head()
# print fireball_df.head()

# #preprocessing - inlcude sightings only bw 1/1/2005 and 9/22/2016
# for index, row in circle_df.iterrows():
#     try:
#         datetimesighting = parser.parse(row['Date / Time'])
#         print datetimesighting
#         # print "this ran"
#         # if (datetime.date(2005, 1, 1) <= datetimesighting <= datetime.date(2015, 9, 22)):
#         #     print "in range"
#         # else:
#         #     print "not in range"
#     except:
#     	print "something"

#preprocessing - nicer format 'duration', 'duration' to seconds

##box plot of duration

##time series pot of number of sightings

##bar chart of sightings

##normalizing by state population
#Population data from US census
population_api = requests.get('http://api.census.gov/data/2015/acs1/cprofile?get=CP05_2015_001E,NAME&for=state:*')
population = population_api.text


