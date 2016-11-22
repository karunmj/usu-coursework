# Example of calling GetSiteInfoObject from a WaterOneFlow web service
from suds.client import Client

# Create a new object named "NWIS" for calling the web
# service methods using the suds client module
NWIS = Client('http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL').service

# Call the GetSiteInfoObject method
response = NWIS.GetSiteInfoObject('NWISUV:10109000')

# Get the site's name from the response
siteName = response.site[0].siteInfo.siteName

# Print the site's name to the console
print siteName

# (this should produce the following output)
# LOGAN RIVER ABOVE STATE DAM, NEAR LOGAN, UT
