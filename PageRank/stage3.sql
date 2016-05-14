
-- *******************************************************************
-- * writeout stage
-- *******************************************************************

DROP TABLE final_results;
DROP TABLE final_scores;

CREATE EXTERNAL TABLE final_results (ts BIGINT, tot_ranks DOUBLE) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES terminated by '\n' STORED AS TEXTFILE LOCATION '${hiveconf:resultspath}';

CREATE EXTERNAL TABLE final_scores (horse STRING, rank DOUBLE, out_degree bigint) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LINES terminated by '\n' STORED AS TEXTFILE LOCATION '${hiveconf:scorepath}';

INSERT OVERWRITE TABLE final_results SELECT * FROM monitering;

INSERT OVERWRITE TABLE final_scores SELECT * FROM horse_ranks;



