import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle 
import datetime
from dateutil import parser
import json
import numpy as np
from sklearn import tree
import pydotplus

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

#timeframe formatting
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

#combine circle, triangle, fireball dataframe
allshape_df = circle_df.append([triangle_df, fireball_df], ignore_index=True)

#preprocessing - include sightings only bw 1/1/2005 and 9/22/2016. New column 'in_range' will be set to 1 if true
in_range=[]
datetimesightingarray=[]
for index, row in allshape_df.iterrows():
    try:
        datetimesighting = parser.parse(row['Date / Time'])
        datetimesightingarray.append(datetimesighting)
        if (datetime.datetime(2005, 1, 1) <= datetimesighting <= datetime.datetime(2016, 9, 23)):
            in_range.append(1)
        else:
            in_range.append(0)
    except:
        in_range.append(0)
        datetimesightingarray.append(np.nan)

allshape_df['in range'] = in_range
allshape_df['datetimesighting'] = datetimesightingarray

#newdata frame to hold in range duration rows only
allshape_inrange_df=(pd.DataFrame([row for index, row in allshape_df.iterrows() if row['in range']==1])).reset_index(drop=True)
allshape_inrange_df = (allshape_inrange_df.sort_values('datetimesighting')).reset_index(drop=True)

##preprocessing - nicer format 'duration', 'duration' to seconds
#TODO

##preprocessing - take out outside us locations, create region column
stateregion = json.load(open('stateregion.json'))

#TODO: this is ugly. use list comprehension to create list and make it a dataframe only in the final step
allshape_inrange_us_df = pd.DataFrame(columns=list(allshape_inrange_df.columns.values))
for index, row in allshape_inrange_df.iterrows():
    if row.State in [stateid for stateid in stateregion['states']]:
        allshape_inrange_us_df=allshape_inrange_us_df.append(row, ignore_index=True)

region = []
for index, row in allshape_inrange_us_df.iterrows():
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
daypart = []
for index, row in allshape_inrange_us_df.iterrows():
    if datetime.time(00,00) <= row['datetimesighting'].time() <= datetime.time(05,59):
        daypart.append('night')
    elif datetime.time(06,00) <= row['datetimesighting'].time() <= datetime.time(11,59):
        daypart.append('morning')
    elif datetime.time(12,00) <= row['datetimesighting'].time() <= datetime.time(17,59):
        daypart.append('afternoon')
    elif datetime.time(18,00) <= row['datetimesighting'].time() <= datetime.time(23,59):
        daypart.append('evening')

allshape_inrange_us_df['time_of_day']=daypart

##creating training(1/1/2005 and 12/31/2013) and test (1/1/2014 and 9/22/2016)set
#index of first row with 2014, 1, 1 as datetime
split_index = allshape_inrange_us_df[allshape_inrange_us_df['datetimesighting'] == datetime.date(2014,1,1)].index[0]

#redundant from below variable, uncomment for debugging datetimesighting
# training_set = allshape_inrange_us_df[0:split_index][['datetimesighting' ,'time_of_day', 'region', 'Shape']].reset_index(drop=True)
# test_set = allshape_inrange_us_df[split_index:][['datetimesighting', 'time_of_day', 'region', 'Shape']].reset_index(drop=True)

training_set = allshape_inrange_us_df[0:split_index][['time_of_day', 'region', 'Shape']].reset_index(drop=True)
test_set = allshape_inrange_us_df[split_index:][['time_of_day', 'region', 'Shape']].reset_index(drop=True)

#Function to map unique attributes to integers
def map_to_integer(df):
    df_mod = df.copy()
    unique_labels = [df_mod[column].unique() for column in df]
    map_to_int = [{name: n for n, name in enumerate(labels)} for labels in unique_labels]
    #unpacking list to a single dict
    map_to_int_unlisted = { k: v for d in map_to_int for k, v in d.items() }
    for column in df:
        df_mod[column+'_mapping'] = df_mod[column].replace(map_to_int_unlisted)
    return (df_mod, map_to_int, unique_labels)

df1, map_to_int, unique_labels = map_to_integer(training_set)
df2, map_to_int, unique_labels = map_to_integer(test_set)

training_set = df1
test_set = df2

#Example code for iris 
from sklearn.datasets import load_iris
iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

dot_data = tree.export_graphviz(clf, out_file=None) 
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("iris.pdf") 

##decision tree illustration
##accuracy table
