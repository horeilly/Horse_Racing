-- ******************************************
-- * worst beatdowns
-- * ****************************************

select * from edge_table order by tot_weight desc limit 100;


-- ******************************************
-- * worst beatdowns
-- * ****************************************

select avg(tot_weight) from edge_table;

	-- 1.0070444407141343

-- ******************************************
-- * most prolificly good horses
-- * ****************************************

select winner, count(*) as tot_pwns from edge_table group by winner order by tot_pwns desc limit 5;

	-- Topton	1177
	-- Palacegate Touch	1137
	-- First Maite	1126
	-- Sharp Hat	1103
	-- Redoubtable	1085

-- ******************************************
-- * most prolificly bad horses
-- * ****************************************

select loser, count(*) as tot_pwns from edge_table group by loser order by tot_pwns desc limit 5;

	-- Marengo I	923
	-- Redoubtable	880
	-- Paddywack	820
	-- Sharp Hat	814
	-- Gone'N'Dunnett	748
