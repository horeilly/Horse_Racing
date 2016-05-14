-- *******************************************************************
-- * setup stage
-- *******************************************************************

SET hive.cli.print.header=true;
-- * set dampener level
SET dampener=0.85;
-- * set s3 location of edges csv file
SET x=s3://horses/edgelist/edges/;
-- * set s3 location of output file
SET outpath=s3://horses/hive/;
SET scorepath=${hiveconf:outpath}scores20;
SET resultspath=${hiveconf:outpath}results20;


-- vectorization????
-- set hive.vectorized.execution.enabled = true;
-- set hive.vectorized.execution.reduce.enabled = true;


-- * clear environment 
DROP TABLE temp_edges;
DROP TABLE edges;
DROP TABLE Horse_Ranks;

-- * load csv into external table
CREATE EXTERNAL TABLE temp_edges (winner STRING, loser STRING, weight INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION '${hiveconf:x}';

-- * create local table from external table
-- * use ORC and cluster by winner for optimization
CREATE TABLE edges STORED AS ORC AS SELECT * FROM temp_edges CLUSTER BY winner;

-- * drop the temporary table
DROP TABLE temp_edges;

-- * initialize ranks table for all horses
DROP TABLE Horse_Ranks;

CREATE TABLE Horse_Ranks STORED AS ORC AS SELECT loser AS horse, 1.0 AS rank, SUM(weight) AS out_degree FROM edges GROUP BY loser ORDER BY horse;

-- * initialize ranks table for horses that have never won 
-- * (for unioning later, to ensure we don't lose horses on iteration)
DROP TABLE Losers_Ranks;

CREATE TABLE Losers_Ranks STORED AS ORC AS SELECT losers.horse AS horse, (1-${hiveconf:dampener}) AS rank, losers.out_degree as out_degree FROM (SELECT DISTINCT winner AS horse FROM edges) AS winners RIGHT OUTER JOIN Horse_Ranks AS losers ON (winners.horse = losers.horse) WHERE ISNULL(winners.horse);

-- * set up table for comparing scores and measuring convergence and timing

DROP TABLE monitering;
CREATE TABLE monitering (ts TIMESTAMP, tot_diffs DOUBLE);

DROP TABLE prev_table;
CREATE TABLE prev_ranks AS SELECT * FROM horse_ranks;




