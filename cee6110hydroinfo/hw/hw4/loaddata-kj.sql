USE odm;

-- load sites
LOAD DATA LOCAL INFILE '/Users/karunjoseph/usu/usu-coursework/cee6110hydroinfo/hw/hw4/Hydroinformatics_Assignment-4_Data/sites.csv'
INTO TABLE sites
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(SiteCode,SiteName,Latitude,Longitude,LatLongDatumID,Elevation_m,VerticalDatum,LocalX,LocalY,LocalProjectionID,PosAccuracy_m,State,County,Comments,SiteType);

-- load source file
-- load water temp file