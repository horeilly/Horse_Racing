import json
import csv

data = list()
with open("horses.json", "rb") as f:
	for line in f:
		data.append(json.loads(line))

print "... DATA LOADED ..."

with open("horses.csv", "wb") as f:
	horsewriter = csv.writer(f)
	horsewriter.writerow(["time", "racecourse", "distance", "going", "name", "position", "jockey",
		"trainer", "sp", "country", "weight", "age", "or", "ts"])
	
	for horse in data:
		horsewriter.writerow([horse["time"], horse["racecourse"], horse["distance"], horse["going"], 
			horse["name"], horse["position"], horse["jockey"], horse["trainer"], horse["sp"], 
			horse["country"], horse["weight"], horse["age"], horse["or"], horse["ts"]])
		print data.index(horse)