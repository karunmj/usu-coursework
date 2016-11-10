"""
Author: Jeff Horsburgh
Created: 10-18-2016
Description: Script to download the most recent discharge
value from a USGS streamflow gage. Developed with students
in the Hydroinformatics class.
"""
import urllib2

# 1. Construct the URL
beginDate = '2016-10-18'
endDate = '2016-10-19'
siteNum = '10109000'
url = 'http://waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no=' + \
      siteNum + '&period=&begin_date=' + beginDate + '&end_date=' + endDate

print url

# 2. Retrieve the file at the URL endpoint
response = urllib2.urlopen(url)

# 3. Read the file into a string
data = response.read()

# 4. Split the file into rows
lines = data.split('\n')

# 5. Get the last row
last_line = lines[-2]

# 6. Split the last line into columns
columns = last_line.split('\t')

# 7. Get the value in the streamflow column
streamFlow = columns[4]
latestDate = columns[2]

outputString = 'The latest provisional value of streamflow at USGS Gage ' + \
               siteNum + ' was ' + streamFlow + ' cfs on ' + latestDate + '.'

# 8. Print the output string to the console
print outputString

# 9. For kicks and giggles - print the last 5 rows of the file to the console.
length = len(lines)
for x in range(-6, -1):
   print lines[x]
