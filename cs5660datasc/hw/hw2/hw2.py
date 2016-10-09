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
import matplotlib.pyplot as plt
import collections
'''
###data collection, pre processing, exploratory analysis

##circle, triangle, fireball data scraping, pickling

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

# pickle.dump(circle_df, open("circle_df.p", "wb"))
# pickle.dump(triangle_df, open("triangle_df.p", "wb"))
# pickle.dump(fireball_df, open("fireball_df.p", "wb"))

# circle_df = pickle.load(open("circle_df.p", "rb"))
# triangle_df = pickle.load(open("triangle_df.p", "rb"))
# fireball_df = pickle.load(open("fireball_df.p", "rb"))

#combine circle, triangle, fireball dataframe
allshape_df = circle_df.append([triangle_df, fireball_df], ignore_index=True)

#preprocessing - include sightings only bw 1/1/2005 and 9/22/2016. New column 'in_range' will be set to 1 if true
in_range=[]
datetimesightingarray=[]
for index, row in allshape_df.iterrows():
    try:
        datetimesighting = parser.parse(row['Date / Time'])
        datetimesightingarray.append(datetimesighting)
        if (datetime.datetime(2005, 1, 1) <= datetimesighting < datetime.datetime(2016, 9, 23)):
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

allshape_inrange_us_df = pd.DataFrame(columns=list(allshape_inrange_df.columns.values))
for index, row in allshape_inrange_df.iterrows():
    if row.State in [stateid for stateid in stateregion['states']]:
        allshape_inrange_us_df=allshape_inrange_us_df.append(row, ignore_index=True)


# pickle.dump(allshape_inrange_us_df, open("allshape_inrange_us_df.p", "wb"))

# allshape_inrange_us_df = pickle.load(open("allshape_inrange_us_df.p", "rb"))

region = []
for index, row in allshape_inrange_us_df.iterrows():
    region.append(stateregion['states'][row.State])

allshape_inrange_us_df['region']=region

##box plot of duration

##time series plot of number of sightings
circle_sighting_df= (pd.DataFrame([row for index, row in allshape_inrange_us_df.iterrows() if row['Shape']=='Circle'])).reset_index(drop=True)
circle_unique_year_number = dict()
for index, row in circle_sighting_df.iterrows():
    if row['datetimesighting'].year in circle_unique_year_number.keys():
        circle_unique_year_number[row['datetimesighting'].year]+=1
    else:
        circle_unique_year_number[row['datetimesighting'].year]=1 
circle_unique_year_number = collections.OrderedDict(sorted(circle_unique_year_number.items()))

triangle_sighting_df= (pd.DataFrame([row for index, row in allshape_inrange_us_df.iterrows() if row['Shape']=='Triangle'])).reset_index(drop=True)
triangle_unique_year_number = dict()
for index, row in triangle_sighting_df.iterrows():
    if row['datetimesighting'].year in triangle_unique_year_number.keys():
        triangle_unique_year_number[row['datetimesighting'].year]+=1
    else:
        triangle_unique_year_number[row['datetimesighting'].year]=1 
triangle_unique_year_number=collections.OrderedDict(sorted(triangle_unique_year_number.items()))

fireball_sighting_df= (pd.DataFrame([row for index, row in allshape_inrange_us_df.iterrows() if row['Shape']=='Fireball'])).reset_index(drop=True)
fireball_unique_year_number = dict()
for index, row in fireball_sighting_df.iterrows():
    if row['datetimesighting'].year in fireball_unique_year_number.keys():
        fireball_unique_year_number[row['datetimesighting'].year]+=1
    else:
        fireball_unique_year_number[row['datetimesighting'].year]=1 
fireball_unique_year_number=collections.OrderedDict(sorted(fireball_unique_year_number.items()))

plt.title('Time series figure with the number of sightings per year (one line per shape)')
plt.ylabel('Number of sightings')
plt.xlabel('Year')
plt.plot(circle_unique_year_number.keys(), circle_unique_year_number.values(), 'r--', triangle_unique_year_number.keys(), triangle_unique_year_number.values(), 'bs-', fireball_unique_year_number.keys(), fireball_unique_year_number.values(), 'g^-.')
plt.legend(['Circle', 'Triangle', 'Fireball'], loc = 'lower right')
plt.show()

##bar chart of sightings per state
state_sighting = dict()
for index, row in allshape_inrange_us_df.iterrows():
    if row['State'] in state_sighting.keys():
        state_sighting[row['State']]+=1
    else:
        state_sighting[row['State']]=1 

plt.bar(np.arange(len(state_sighting)), state_sighting.values(), align='center', width = 0.4)
plt.xticks(np.arange(len(state_sighting)), state_sighting.keys(), rotation='vertical')
plt.ylabel('Number of sightings')
plt.title('Bar chart of sightings per state between 1/2005-9/2016') 
plt.show()

##normalizing by state population
#Population data from US census
population_api = requests.get('http://api.census.gov/data/2015/acs1/cprofile?get=CP05_2015_001E,NAME&for=state:*')
population = population_api.json()[1:]
population_dict = {row[1]: row[0] for index, row in enumerate(population)}
state_sighting_pop_norm  = {k: v/float(population_dict[stateregion['state_code'][k]]) for k, v in state_sighting.iteritems()}

plt.bar(np.arange(len(state_sighting_pop_norm)), state_sighting_pop_norm.values(), align='center', width = 0.4)
plt.xticks(np.arange(len(state_sighting_pop_norm)), state_sighting_pop_norm.keys(), rotation='vertical')
plt.ylabel('Number of sightings normalized by population')
plt.title('Bar chart of sightings normalized per state population between 1/2005-9/2016') 
plt.show()

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

#redundant from below variable, uncomment for debugging datetimesighting. remove later
# training_set = allshape_inrange_us_df[0:split_index][['datetimesighting' ,'time_of_day', 'region', 'Shape']].reset_index(drop=True)
# test_set = allshape_inrange_us_df[split_index:][['datetimesighting', 'time_of_day', 'region', 'Shape']].reset_index(drop=True)

training_set = allshape_inrange_us_df[0:split_index][['time_of_day', 'region', 'Shape']].reset_index(drop=True)
test_set = allshape_inrange_us_df[split_index:][['time_of_day', 'region', 'Shape']].reset_index(drop=True)

pickle.dump(training_set, open("training_set.p", "wb"))
pickle.dump(test_set, open("test_set.p", "wb"))
'''
training_set = pickle.load(open("training_set.p", "rb"))
test_set = pickle.load(open("test_set.p", "rb"))

#scikit-learn doesn't support categorical values, they need to be vectorized
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()


#Function to map unique attributes to integers
#Not correct way
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

##Fitting training data to a decision tree classifier
# #Example code for iris 
from sklearn.datasets import load_iris
iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

training_data = training_set.as_matrix(columns=['time_of_day_mapping', 'region_mapping'])
training_target = np.array(training_set['Shape_mapping'].tolist())

clf = clf.fit(training_data, training_target)

##decision tree illustration
#dot_data = tree.export_graphviz(clf, out_file=None, feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True, special_characters=True) 
dot_data = tree.export_graphviz(clf, out_file=None, feature_names=list(training_set[['time_of_day_mapping', 'region_mapping']].columns.values), class_names= unique_labels[2], filled=True, rounded=True, special_characters=True) 

'''
import sys
reload (sys)
sys.setdefaultencoding('utf8')
'''
graph = pydotplus.graph_from_dot_data(dot_data) 
graph.write_pdf("ufo_tree.pdf") 
#graph.write_pdf("iris.pdf")

##accuracy table
