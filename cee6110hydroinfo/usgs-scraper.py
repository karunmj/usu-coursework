import requests
import urllib2

cherrycreek_url = 'http://waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no=06713500&period=&begin_date=2016-10-18&end_date=2016-10-18'
cherrycreek_url_req = requests.get(cherrycreek_url)

beginDate = '2016-10-18'
endDate = '2016-10-19'
siteID = '06713500'

url = 'http://waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no=' + siteID + '&period=&begin_date=' + beginDate + '&end_date=' + endDate

response = urllib2.urlopen(url)
data = response.read()
lines = data.split('\n')

last_row = lines[-2]

last_row_elements = last_row.split('\t')

streamflow = last_row_elements[4]

