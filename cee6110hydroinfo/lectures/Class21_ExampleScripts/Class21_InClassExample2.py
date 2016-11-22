# Example of calling GetValuesObject from a WaterOneFlow web service
from suds.client import Client
from pandas import Series

# Create the inputs needed for the web service call
wsdlURL = 'http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL'
siteCode = 'NWISUV:10109000'
variableCode = 'NWISUV:00060'
beginDate = '2016-10-20'
endDate = '2016-11-07'

# Create a new object named "NWIS" for calling the web service methods
NWIS = Client(wsdlURL).service

# Call the GetValuesObject method to return datavalues
response = NWIS.GetValuesObject(siteCode, variableCode, beginDate, endDate)

# Get the site's name from the response
siteName = response.timeSeries[0].sourceInfo.siteName

# Create some blank lists in which to put the values and their dates
a = []  # The values
b = []  # The dates

# Get the values and their dates from the web service response
values = response.timeSeries[0].values[0].value

# Loop through the values and load into the blank lists using append
for v in values:
    a.append(float(v.value))
    b.append(v._dateTime)

# Create a Pandas Series object from the lists
# Set the index of the Series object to the dates
ts = Series(a, index=b)

# Get the site's minimum streamflow value and datetime of occurrence to the console
minFlow = ts.min()
dateOfMin = ts.idxmin()
print 'Minimum streamflow at %s was %s cfs on %s' % (siteName, minFlow, dateOfMin)
# This should produce output similar to:
# "Minimum streamflow at LOGAN RIVER ABOVE STATE DAM, NEAR LOGAN, UT was 81.0 cfs on 2015-10-21 10:45:00"

