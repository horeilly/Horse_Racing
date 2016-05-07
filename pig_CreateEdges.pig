-- ************************************************
-- * Create an edge list from horse_races table
-- * 
-- * 	- Make sure to read from hive table using:
-- *
-- * 		pig -useHCatalog
-- * 
-- ************************************************

HIVE_TABLE = LOAD 'horse_races' USING org.apache.hive.hcatalog.pig.HCatLoader();

RACES = GROUP HIVE_TABLE BY (race_datetime, racecourse);

RACES = FOREACH RACES GENERATE HIVE_TABLE AS ONE_RACE;





