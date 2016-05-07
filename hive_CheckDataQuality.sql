-- *******************************************************
-- * Load data from scatch to check data quality
-- *******************************************************

-- * setup configuration, show the column names

set hive.cli.print.header=true;

-- * load temp external table, use strings on everything for now
-- * until we have better picture of data quality

create databases horses;
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

-- ************************************
-- * EDA on temp table for data quality
-- ************************************

-- check to see if we have irregular distances, positions, weights, ages, and orders
select *, cast(Distance as float) as dist 
	from temphorses 
	order by dist asc 
	limit 5;
	-- **************************************
	-- we have some distances of 0.0, weird
	-- **************************************

select *, cast(Distance as float) as dist 
	from temphorses 
	order by dist desc 
	limit 5;
	-- normal

select *, cast(position as float) as pos 
	from temphorses 
	order by pos asc 
	limit 5;
	-- **************************************
	-- we have positions of 0, which is weird
	-- **************************************

select *, cast(position as float) as pos 
	from temphorses 
	order by pos desc 
	limit 5;
	-- seems normal

select *, cast(weight as float) as wei 
	from temphorses 
	order by wei asc 
	limit 5;
	-- **************************************
	-- CRAP! we have some trainer names with commas in them,
	-- we need to delimiate them with something different and wierd
	-- **************************************

select *, cast(weight as float) as wei 
	from temphorses 
	order by wei desc 
	limit 5;
	-- ?? not done yet

select *, cast(age as float) as ayge 
	from temphorses 
	order by ayge desc 
	limit 5;
	-- ?? not done yet

select *, cast(age as float) as ayge 
	from temphorses 
	order by ayge desc 
	limit 5;
	-- ?? not done yet

select *, cast(order as float) as ord 
	from temphorses 
	order by ord desc 
	limit 5;
	-- ?? not done yet


