-- ************************************************
-- * Create ORC hive table from an S3 csv 
-- * 		- Make sure that CSV has header removed
-- * 		- Will produce a table named horse_races
-- * 		- in a horses database
-- ************************************************


-- * setup configuration, show the column names

set hive.cli.print.header=true;


-- ************************************************
-- * Create database
-- ************************************************

CREATE DATABASE horses;


-- ************************************************
--- * Create temporary external table to read data from
-- ************************************************

DROP TABLE temphorses;

CREATE EXTERNAL TABLE temphorses (Race_DateTime STRING, 
								Racecourse STRING, 
								Ground STRING, 
								Distance STRING, 
								Horse STRING, 
								Position STRING, 
								Jockey STRING, 
								Trainer STRING, 
								Weight STRING, 
								Age STRING, 
								Country STRING, 
								Order STRING)
		ROW FORMAT 
		DELIMITED FIELDS TERMINATED BY ',' 
		LINES TERMINATED BY '\n' 
		LOCATION 's3://horses/hive_external/';

-- * alternative format, above format causes problems with copy/paste
-- * CREATE EXTERNAL TABLE temphorses (Race_DateTime STRING, Racecourse STRING, Ground STRING, Distance STRING, Horse STRING, Position STRING, Jockey STRING, Trainer STRING, Weight STRING, Age STRING, Country STRING, Order STRING) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' LOCATION 's3://horses/hive_external/';


-- ************************************************
-- * Create table for to prepare ingesting raw csv
-- ************************************************

DROP TABLE horse_races;

CREATE TABLE horse_races (Race_DateTime TIMESTAMP,
							Racecourse STRING,
							Ground STRING,
							Distance FLOAT,
							Horse STRING,
							Position BIGINT,
							Jockey STRING,
							Trainer STRING,
							Weight FLOAT,
							Age BIGINT,
							Country STRING,
							Order STRING) STORED AS ORC;

-- * alternative format, above format causes problems with copy/paste
-- * CREATE TABLE horse_races (Race_DateTime TIMESTAMP, Racecourse STRING, Ground STRING, Distance FLOAT, Horse STRING, Position BIGINT, Jockey STRING, Trainer STRING, Weight FLOAT, Age BIGINT, Country STRING, Order STRING) STORED AS ORC;


-- ************************************************
-- * Load data into table from temp table
-- ************************************************

INSERT INTO TABLE horse_races SELECT * FROM temphorses;

-- * alternative format, above format causes problems with copy/paste
-- * INSERT INTO TABLE horse_races (Race_DateTime TIMESTAMP, Racecourse STRING, Ground STRING, Distance FLOAT, Horse STRING, Position BIGINT, Jockey STRING, Trainer STRING, Weight FLOAT, Age BIGINT, Country STRING, Order STRING) SELECT * FROM temphorses;

-- * drop old external table

DROP TABLE temphorses;


