
-- *******************************************************************
-- * iteration stage
-- *******************************************************************

-- * update horse_ranks
INSERT OVERWRITE TABLE horse_ranks SELECT * FROM (SELECT new.horse AS horse, new.rank AS rank, old.out_degree AS out_degree FROM (SELECT horse, (1-${hiveconf:dampener}) + ${hiveconf:dampener}*SUM(item) AS rank FROM (SELECT edges.winner AS horse, edges.weight*(ranks.rank/ranks.out_degree) AS item FROM edges AS edges JOIN horse_ranks AS ranks ON (edges.loser = ranks.horse)) AS foo GROUP BY horse) AS new JOIN horse_ranks AS old ON (new.horse = old.horse) UNION ALL SELECT * FROM losers_ranks) AS unionResult;

-- ********************
-- * update explanation
-- ********************

-- SELECT * FROM 
-- 	(SELECT new.horse AS horse, new.rank AS rank, old.out_degree AS out_degree 
-- 		FROM 
-- 		(SELECT horse, (1-${hiveconf:dampener}) + ${hiveconf:dampener}*SUM(item) AS rank 
-- 			FROM 
-- 			(SELECT edges.winner AS horse, edges.weight*(ranks.rank/ranks.out_degree) AS item 
-- 				FROM 
-- 					edges AS edges 
-- 				JOIN 
-- 					horse_ranks AS ranks 
-- 				ON (edges.loser = ranks.horse)) AS foo 
-- 			GROUP BY horse) AS new 
-- 		JOIN 
-- 			horse_ranks AS old 
-- 		ON (new.horse = old.horse) 
-- 	UNION ALL SELECT * FROM losers_ranks) AS unionResult;

-- first, join edges to ranks, and then calculate (rank/outdegree) for 
-- each losing horse, mulitplying by weight, then group by winning horse
-- and sum each score, multiplying/adding with dampener. 
-- join this result with prevoius rank table to get out_degrees for each 
-- horse, and then union result with table of horses that never won a 
-- race to produce new horse_rank table with same number of rows

-- * update monitering with new ranks
INSERT INTO TABLE monitering SELECT unix_timestamp() AS ts, SUM(diff) AS tot_diffs FROM (SELECT prev.horse AS horse, ABS(prev.rank - curr.rank) AS diff FROM prev_ranks AS prev JOIN horse_ranks AS curr ON (prev.horse = curr.horse)) AS foo;

INSERT OVERWRITE TABLE prev_ranks SELECT * FROM horse_ranks;




