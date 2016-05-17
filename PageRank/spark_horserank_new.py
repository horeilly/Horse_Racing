
#### NOTE, i'm not filtering out the (nobody, won, -132334) record yet
#### because I'm lazy, but just do it at the beginning in the future



# start spark with extra driver memory
# 		pyspark --driver-memory 3G

# set up S3 access

sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", AWS_ACCESS_KEY_ID)
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey",AWS_SECRET_ACCESS_KEY)

# import dependencies
import sys
import time
from operator import add

# set number of iterations
iterations = 50

# load data from sc3
edges = sc.textFile("s3://horses/edgelist/edges/")

# prepare your dampener as BROADCAST VARIABLE
dampener = 0.85
dscore = sc.broadcast(dampener)
	# dscore is BROADCAST VARIABLE

# prepare initial horse-scores dictionary as BROADCAST VARIABLE
winners = edges.map(lambda x: (x.split(',')[0], 1))
losers = edges.map(lambda x: (x.split(',')[1], 1))
horses = winners.union(losers)
horsesdict = horses.collectAsMap()
	# for checking size of horsedict, to ensure space constraints for broadcasting
		#len(horsesdict)
		#sys.getsizeof(horsesdict)
horses = sc.broadcast(horsesdict)
	# horses is a BROADCAST VARIABLE

# prepare loser-scores dictionary as a LOCAL variable, won't need it on the executors
winner_list = winners.map(lambda x: x[0]).collect()
winner_list = set(winner_list)
loser_dict = losers.filter(lambda x: x[0] not in winner_list).map(lambda x: (x[0], dscore.value)).collectAsMap()

# prepare outlinks dictionary as a BROADCAST VARIABLE
out_dict = edges.map(lambda x: (x.split(',')[1], int(x.split(',')[2]))).reduceByKey(add).collectAsMap()
outlinks = sc.broadcast(out_dict)
	# outlinks is a BROADCAST VARIABLE

edgesRDD = edges.map(lambda x: (x.split(',')[0], (x.split(',')[1], int(x.split(',')[2])))).cache()
	# prepare an edges RDD and cache it since you'll use it at every stage

diffs = []

##### above is the setup stage ######

starttime = time.time()
for i in range(0,iterations):
	eachScoreRDD = edgesRDD.map(lambda x: (x[0], dscore.value*x[1][1]*(horses.value[x[1][0]]/float(outlinks.value[x[1][0]]))))
	sumScoreRDD = eachScoreRDD.reduceByKey(add)
	ScoreRDD = sumScoreRDD.map(lambda x: (x[0], x[1] + (1-dscore.value)))
	new_horsesdict = ScoreRDD.collectAsMap()
	new_horsesdict.update(loser_dict)
	tot_diff = 0
	for i in horsesdict.keys():
		tot_diff += abs(horsesdict[i] - new_horsesdict[i])
	diffs.append(tot_diff)
	del horsesdict
	horses.unpersist()
	horsesdict = new_horsesdict
	horses = sc.broadcast(horsesdict)





endtime = time.time()

# total time it takes to run all X iterations
print endtime - starttime


# save results to file
final_results = sc.parallelize(diffs)
final_results = final_results.coalesce(1)
final_results.saveAsTextFile("s3://horses/edgelist/spark_results2/")

final_horsescores = sc.parallelize(horsesdict.items())
final_horsescores = final_horsescores.coalesce(1)
final_horsescores.saveAsTextFile("s3://horses/edgelist/spark_horseranks2/")

