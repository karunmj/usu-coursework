import pymysql
from matplotlib import pyplot, dates
import numpy as np
import datetime

##Open connection to db
cnxn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd="", db='loganriverodm')
crsr = cnxn.cursor()


##Perform queries
#1. How many temperature observations are there in the Logan River ODM database?
crsr.execute("SELECT * FROM loganriverodm.DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1")
row=crsr.fetchall()
totaltempnumber = len(row) #144466

#2. What Percent of the Temperature Data in LoganRiverODM are Null?
crsr.execute("SELECT * FROM loganriverodm.Datavalues WHERE VariableID = 57 AND DataValue = -9999 AND QualityControlLevelID = 1")
row=crsr.fetchall()
nulltempnumber = len(row) #652
nulltempperc = float(nulltempnumber)/totaltempnumber #0.0045131726496199795

#3. What percent of the (non-null) temperature observations are > 20 degrees?
crsr.execute("SELECT * FROM loganriverodm.DataValues WHERE VariableID = 57 AND DataValue <> -9999 AND QualityControlLevelID = 1")
row=crsr.fetchall()
nonnulltempnumber = len(row) #143814

crsr.execute("SELECT * FROM loganriverodm.DataValues WHERE VariableID = 57 AND DataValue <> -9999 AND DataValue > 20 AND QualityControlLevelID = 1")
row=crsr.fetchall()
twentygreatertempnumber = len(row) #818
percenttwenty = (float(twentygreatertempnumber)/nonnulltempnumber)*100 #0.5687902429527028

#4. What is the average temperature at midnight? (hint, the return type for a date retrieved from pymysql is also a date type. So you can use functions like, "myvalue.year" to get an integer representation of the year. 
crsr.execute("SELECT * FROM loganriverodm.DataValues WHERE VariableID = 57 AND DataValue <> -9999 AND TIME(LocalDateTime) = MAKETIME(00,00,00) AND QualityControlLevelID = 1 ORDER BY LocalDateTime ASC")
row=crsr.fetchall()
avgtemp = np.mean([element[1] for element in row]) #7.7669107856191744

#5. Make a graph of the data (not including null values) using matplotlib. My code shows a very simple graph using matplotlib. Your graph should include a date on the x axis, a y axis label and an appropriate title. You can find examples here
pyplot.title('Daily midnight water temperature at Logan River')
pyplot.ylabel('Water temperature (degree celsius)')
pyplot.xlabel('Local date time')
pyplot.plot([element[1] for element in row])
pyplot.xticks(range(len([element[1] for element in row]))[0::120], [element[3].strftime('%m/%d/%Y') for element in row][0::120], rotation = 22)
pyplot.show()


##Close connection to db
cnxn.close()


