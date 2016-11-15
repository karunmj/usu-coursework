USE loganriverodm;

-- check if datavalues were loaded 
SELECT COUNT(*) FROM datavalues;

/*
Q1. A table listing the period of record for water temperature measurements (e.g., begin
and end date), the number of observations, and the overall minimum, maximum,
and average values for each site at which quality controlled (QualityControlLevelID
= 1) water temperature (VariableID = 57) data have been collected.
*/
SELECT SiteID, BeginDateTime, EndDateTime FROM SeriesCatalog WHERE VariableID = 57 AND QualityControlLevelID = 1;
SELECT SiteID, COUNT(DataValue), MAX(DataValue), MIN(DataValue), AVG(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 GROUP BY SiteID; 


/*
Q2. A table listing the total number of temperature observations, the number of
observations greater than the water quality criterion value (i.e., 20 degrees C), and
the overall percent exceedance of the water quality criterion value for each site at
which quality controlled water temperature data have been collected
*/
SELECT SiteID, COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 GROUP BY SiteID;
SELECT SiteID, COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 GROUP BY SiteID;
-- Only SiteID = 2 has above 20 deg c temps
SELECT SiteID, COUNT(DataValue)/(SELECT COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND SiteID = 2) FROM datavalues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 GROUP BY SiteID;


/*
Q3 A table for the Logan River at Mendon Road (SiteID = 2) listing the percent
exceedance of the water quality standard for each month of the year.
*/
SELECT SiteID, COUNT(DataValue), MONTH(LocalDateTime) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 AND SiteID = 2 GROUP BY MONTH(LocalDateTime);
-- Months where temp increases are July (7), August (8)
SELECT COUNT(DataValue)/(SELECT COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND SiteID = 2 AND MONTH(LocalDateTime) = 7) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 AND SiteID = 2 AND MONTH(LocalDateTime) = 7; 
SELECT COUNT(DataValue)/(SELECT COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND SiteID = 2 AND MONTH(LocalDateTime) = 8) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 AND SiteID = 2 AND MONTH(LocalDateTime) = 8; 


/*
Q4, A table listing the percent exceedance of the water quality standard for each site at
which quality controlled data are available during the month of July, which is
generally a critical period with low flows and elevated temperatures.
*/
SELECT COUNT(DataValue)/(SELECT COUNT(DataValue) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND SiteID = 2 AND MONTH(LocalDateTime) = 7) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND DataValue > 20 AND SiteID = 2 AND MONTH(LocalDateTime) = 7; 

SELECT DataValue, MONTH(LocalDateTime), TIME(LocalDateTime) FROM DataValues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999 AND SiteID = 2 AND MONTH(LocalDateTime) = 7;
