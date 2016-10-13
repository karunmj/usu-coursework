USE loganriverodm;

-- load sites
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw5/Hydroinformatics_Assignment-5_Data/datavalues.csv'
INTO TABLE DataValues
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(DataValue,LocalDateTime,UTCOffset,DateTimeUTC,SiteID,VariableID,CensorCode,QualifierID,MethodID,SourceID,QualityControlLevelID);

SELECT COUNT(*) FROM datavalues