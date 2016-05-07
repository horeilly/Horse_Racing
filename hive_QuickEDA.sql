-- ******************************************
-- * oldest race in database
-- * ****************************************

SELECT min(race_datetime) FROM horse_races;

	-- oldest race is on 1985-06-08 11:02:00


-- * ****************************************
-- * newest race in database
-- * ****************************************

SELECT max(race_datetime) FROM horse_races;

	-- most recent race is 2016-02-27 19:00:00


-- * ****************************************
-- * types of grounds
-- * ****************************************

SELECT DISTINCT ground FROM horse_races;

	-- the types of grounds are: 	ground
							--		Fast
							--		Firm
							--		Frozen
							--		Good
							--		Good To Firm
							--		Good To Soft
							--		Hard
							--		Heavy
							--		Holding
							--		Muddy
							--		NA
							--		Sloppy
							--		Slow
							--		Soft
							--		Standard
							--		Yielding

-- * ****************************************
-- * maximum distance of the horse races
-- * ****************************************

SELECT max(distance) FROM horse_races;

	-- 4.563

-- * ****************************************
-- * smallest distance race
-- * ****************************************

SELECT min(distance) FROM horse_races;

	-- 0.0

-- * ****************************************
-- * average distance
-- * ****************************************

SELECT avg(distance) FROM horse_races;

	-- 1.5870186486295512

-- * ****************************************
-- * number of horses
-- * ****************************************

select count(*) FROM (SELECT DISTINCT horse FROM horse_races) as FOO;

	-- 374,319 horses

-- * ****************************************
-- * number of racecourses
-- * ****************************************

select count(*) FROM (SELECT DISTINCT racecourse FROM horse_races) as FOO;

	-- 1,027 racecourses

-- * ****************************************
-- * number of actual races
-- * ****************************************

select count(*) FROM (SELECT DISTINCT race_datetime, racecourse  FROM horse_races) as FOO;

	-- 437,336 individual races

