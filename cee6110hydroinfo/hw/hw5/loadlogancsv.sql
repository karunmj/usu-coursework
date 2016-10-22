USE loganriverodm;

-- load datavalues
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw5/Hydroinformatics_Assignment-5_Data/datavalues.csv'
INTO TABLE DataValues
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(DataValue,LocalDateTime,UTCOffset,DateTimeUTC,SiteID,VariableID,CensorCode,QualifierID,MethodID,SourceID,QualityControlLevelID);

-- check if datavalues were loaded 
SELECT COUNT(*) FROM datavalues

-- Q1. Period of record, number, max, min, avg of water temp obs. TODO: begin, end date
SELECT COUNT(DataValue), MAX(DataValue), MIN(DataValue), AVG(DataValue) FROM datavalues WHERE VariableID = 57 AND QualityControlLevelID = 1 AND DataValue <> -9999; -- GROUP BY LocalDateTime ;

-- 