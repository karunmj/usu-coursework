__author__ = "Dan Ames"
__date__ = "10/8/2015"
import pymysql
import matplotlib.pyplot as plt

import numpy as np

#Function for getting a list of sites from a HydroServer
def GetSites(VariableID):
        cnxn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd="stevekarun", db='odm')
        crsr = cnxn.cursor()
        q = """
                select Sites.SiteID, Sites.SiteName, min(DataValues.LocalDateTime) as BeginDate, max(DataValues.LocalDateTime) as EndDate,
                count(DataValues.DataValue) as Observations
                from Sites
                        inner join odm.DataValues
                        on odm.Sites.SiteID = odm.DataValues.SiteID
                where DataValues.VariableID =""" + str(VariableID) + """ and odm.DataValues.DataValue <> -9999
                group by Sites.SiteID, odm.Sites.SiteName
                order by Sites.SiteID"""
        crsr.execute(q)

        f = open("GetSites.csv", "w")
        for row in crsr:
                f.write('"' + '","'.join([str(s) for s in row]) + '"')
                f.write('\n')

        f.close()
        cnxn.close()

#Function for getting a data set from a specific site
def GetValues(VariableID, SiteID):
        rows = []
        cnxn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd="stevekarun", db='odm')
        crsr = cnxn.cursor()
        q = """select Sites.SiteID, Sites.SiteName, DataValues.LocalDateTime, DataValues.DataValue
                from Sites
                        inner join DataValues
                        on Sites.SiteID = DataValues.SiteID
                where Sites.SiteID =""" + str(SiteID) + """ and DataValues.VariableID =""" + str(VariableID) + """
				and DataValues.DataValue <> -9999
                group by Sites.SiteID, Sites.SiteName, DataValues.LocalDateTime, DataValues.DataValue
                order by DataValues.LocalDateTime"""

        crsr.execute(q)

        f = open("GetValues.csv", "w")
        for row in crsr:
                f.write('"' + '","'.join([str(s) for s in row]) + '"')
                f.write('\n')
                rows.append(row[3])
        f.close()
        cnxn.close()
        return rows


#Function for getting a list of all  methods in the database
def GetMethods():
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd="stevekarun", db='odm')
        cur = conn.cursor()
        cur.execute("SELECT * FROM methods")
        r = cur.fetchall()


#Function for getting a list of all variables in the database
def GetVariables():
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd="stevekarun", db='odm')
        cur = conn.cursor()
        cur.execute("SELECT * FROM variables")
        r = cur.fetchall()


#***********************************************************************************************************************
#Main Program
#The program starts here. It runs the above functions as needed.
#***********************************************************************************************************************

#get list of methods
GetMethods()

GetVariables()
#find sites that have temp (variable 1)
GetSites(1)
#Download data for variable 1 at site 1 (Mendon Rd)
r = GetValues(1, 2)

print r


#Some very simple example code for using MatPlotLib
#For more examples, see http://matplotlib.org/1.3.1/users/pyplot_tutorial.html
# evenly sampled time at 200ms intervals


# red dashes, blue squares and green triangles
plt.plot(r)  #
plt.show()



