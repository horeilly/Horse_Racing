-- ************************************************
-- * Create an edge list from horse_races table
-- * 
-- * 	- Make sure to read from hive table using:
-- *
-- * 		pig -useHCatalog
-- * 
-- ************************************************

-- * load UDFS and hive table

register 'udfs.py' using jython as pyfunctions;

HIVE_TABLE = LOAD 'horse_races' USING org.apache.hive.hcatalog.pig.HCatLoader();


-- * group rows by races

RACES = GROUP HIVE_TABLE BY (race_datetime, racecourse);

RACES = FOREACH RACES GENERATE group AS RACE_ID, HIVE_TABLE AS ONE_RACE;


-- * use UDF to turn bag of rows into edge list, output bag of edges
-- * flatten bag of edges into rows of edges

EDGE_LIST = FOREACH RACES GENERATE RACE_ID, pyfunctions.get_edges(ONE_RACE);

EDGE_LIST = FOREACH EDGE_LIST GENERATE FLATTEN(edge_bag);


-- * group rows of edges by winner/loser combo
-- * aggregate edge weights, and produce list of weighted edges

EDGES_GROUPED = GROUP EDGE_LIST BY (edge_bag::winner,edge_bag::loser);

TOTAL_EDGES = FOREACH EDGES_GROUPED GENERATE FLATTEN(group) AS (winner, loser), 
						SUM(EDGE_LIST.edge_bag::weight) AS tot_weight;


-- * store edge table into HIVE 
-- * NOTE: hive table must be created prior to running this script!

STORE TOTAL_EDGES INTO 'edge_table' USING org.apache.hive.hcatalog.pig.HCatStorer();

-- * option: store tables into HDFS or S3 instead of into Hive:
-- * 
-- * HDFS: 
-- * 		STORE TOTAL_EDGES INTO '/edgelist' USING PigStorage(',', '-schema');
-- * S3:
-- * 		STORE TOTAL_EDGES INTO 's3://horses/edgelist/edges' USING PigStorage(',', '-schema');



