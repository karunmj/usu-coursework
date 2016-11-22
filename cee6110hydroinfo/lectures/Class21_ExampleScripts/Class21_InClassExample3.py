# Example of calling GetValuesObject from a WaterOneFlow web service
# Then create a time series plot using matplotlib
from suds.client import Client
from pandas import Series
import matplotlib.pyplot as plt

# Create the inputs needed for the web service call
wsdlURL = 'http://hydroportal.cuahsi.org/nwisuv/cuahsi_1_1.asmx?WSDL'
siteCode = 'NWISUV:10105900'
variableCode = 'NWISUV:00060'
beginDate = '2016-10-20'
endDate = '2016-11-06'

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

# Use MatPlotLib to create a plot of the time series
# Create a plot of the streamflow statistics
# ------------------------------------------
# Create a figure object and add a subplot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)  # arguments for add_subplot - add_subplot(nrows, ncols, plot_number)

# Call the plot() methods on the series object to plot the data
ts.plot(color='blue', linestyle='solid', label='15-minute streamflow values')

# Set some properties of the subplot to make it look nice
ax.set_ylabel('Discharge, cubic feet per second')
ax.set_xlabel('Date')
ax.grid(True)
ax.set_title(siteName)

# Add a legend with some customizations
legend = ax.legend(loc='upper left', shadow=True)

# Create a frame around the legend.
frame = legend.get_frame()
frame.set_facecolor('0.95')

# Set the font size in the legend
for label in legend.get_texts():
    label.set_fontsize('large')

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

plt.show()

print 'Done!'

