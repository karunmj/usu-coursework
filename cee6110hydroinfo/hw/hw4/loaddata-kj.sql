USE odm;

-- load sites
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/sites.csv'
INTO TABLE sites
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(SiteCode,SiteName,Latitude,Longitude,LatLongDatumID,Elevation_m,VerticalDatum,LocalX,LocalY,LocalProjectionID,PosAccuracy_m,State,County,Comments,SiteType);

-- load methods file
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/methods.csv'
INTO TABLE methods
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(MethodDescription,MethodLink);

-- load source file
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/sources.csv'
INTO TABLE sources
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(Organization,SourceDescription,SourceLink,ContactName,Phone,Email,Address,City,State,ZipCode,Citation,MetadataID);

-- load variable file 
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/variables.csv'
INTO TABLE variables
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(VariableCode,VariableName,Speciation,VariableUnitsID,SampleMedium,ValueType,IsRegular,TimeSupport,TimeUnitsID,DataType,GeneralCategory,NoDataValue);

-- load temperaturedata file 
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/temperaturedata.csv'
INTO TABLE datavalues
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(DataValue,LocalDateTime,UTCOffset,DateTimeUTC,SiteID,VariableID,MethodID,SourceID,QualityControlLevelID);

-- load ph file 
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/ph.csv'
INTO TABLE datavalues
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(DataValue,LocalDateTime,UTCOffset,DateTimeUTC,SiteID,VariableID,MethodID,SourceID,QualityControlLevelID);


-- load sp file 
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/sp.csv'
INTO TABLE datavalues
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(DataValue,LocalDateTime,UTCOffset,DateTimeUTC,SiteID,VariableID,MethodID,SourceID,QualityControlLevelID);


SET SQL_SAFE_UPDATES = 0;
USE loganriverodm;
CALL sp_UpdateSeriesCatalog();