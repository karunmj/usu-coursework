
###Problem 5

##Importing dataretrieval, ggplot tools
library(dataRetrieval)
library(ggplot2)

##Retrieve daily discharge for last 20 years
siteNo <- "06713500"
pCode <- "00060"
start.date <- "1996-09-01"
end.date <- "2016-09-01"
cherry_creek <- readNWISuv(siteNumbers = siteNo, parameterCd = pCode, startDate = start.date, endDate = end.date)
cherry_creek <-renameNWISColumns(cherry_creek)

#Slicing list to obtain 4th column
#chery_creek_4 <- chery_creek[4]  #this didnt work out

##Daily discharge plot
plotdd <- ggplot(data = cherry_creek, aes(dateTime, Flow_Inst)) + geom_line() #From https://owi.usgs.gov/R/dataRetrieval.html#14. Not familiar with ggplot2




