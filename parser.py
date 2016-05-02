import re
import json
from bs4 import BeautifulSoup

# reads ids corresponding to non races
# with open("non_races.txt", "rb") as f:
#     non_races = f.readlines()

# reads ids corresponding to races with pages issues
# with open("problem_pages.txt", "rb") as f:
#     problem_pages = f.readlines()
#
# with open("no_info.txt", "rb") as f:
#     no_info = f.readlines()

# computes sets of these ids and a set of all ids
# all_races = set([i for i in range(1, 650001)])
# non_races = set([int(i.strip("\n")) for i in non_races])
# problem_pages = set([int(i.strip("\n")) for i in problem_pages])
# no_info = set([int(i.strip("\n")) for i in no_info])

# excludes non race and problem page ids from all ids
# races = all_races.difference(non_races)
# races = races.difference(problem_pages)
# races = list(races.difference(no_info))

with open("valid.txt", "rb") as f:
	valid = f.readlines()

valid = [int(i.strip("\n")) for i in valid]

def get_racecourse(soup):
	try:
		header = soup.title.text.split(" | ")
		racecourse = re.sub(r"Results From The (\d\.|\d\d\.)\d\d Race At ", "", header[0])

		return racecourse
	except Exception:
		return "NA"

def get_time(soup):
	try:
		time = soup.find("div", {"class": "leftColBig"}).find("span", {"class": "timeNavigation"}).text
		time = re.search(r"(\d\d|\d):\d\d", time).group()

		return time
	except AttributeError:
		return "NA"

def get_dist_going(soup):
	dist_going = soup.select("body div div div div.popUp div.popUpHead ul li")
	try:
		dist = re.search(r"\d+[mf]{1}\d*f{0,1}\d*y{0,1}", dist_going[0].text.strip()).group()
	except AttributeError:
		dist = "NA"
	try:
		ground = re.search(r"Good To Firm|Good To Soft|Heavy|Soft|Good|Firm|Hard|Yielding|"
						   r"Standard to Slow|Standard to Fast|Slow|Standard|Fast|"
						   r"Muddy|Sloppy|Frozen|Holding", dist_going[0].text.strip()).group()
	except AttributeError:
		ground = "NA"

	return {"dist": dist, "ground": ground}

def get_position(soup):
	positions = list()
	for position in soup.find_all("td", {"class": "nowrap noPad"}):
		try:
			positions.append(position.text.strip())
		except Exception:
			positions.append("NA")
	return positions

def get_name(soup):
	names = soup.select("tbody tr td b a")
	name_list = list()
	for name in names:
		try:
			name_list.append(name.text)
		except Exception:
			name_list.append("NA")
	return name_list

def get_country_sp(soup):
	css = soup.select("tbody tr td span.black")
	countries = list()
	sps = list()
	for row in css:
		try:
			country = re.search(r"\(\w+\)", row.text).group()
			countries.append("".join([ch for ch in country if ch not in ["(", ")"]]))
		except AttributeError:
			countries.append("UK")
		try:
			sp = re.search(r"\d+/\d+", row.text).group()
			sps.append(sp)
		except AttributeError:
			sps.append("NA")

	return {"country": countries, "sp": sps}

def get_age_weight_trainer(soup):
	awt = list()
	tbl = soup.select("table tbody tr td.black")
	tbls = [tbl[j:j + 3] for j in xrange(0, len(tbl), 3)]
	for row in tbls:
		age = row[0].text
		try:
			weight = re.search(r"\d+-\d+", row[1].text).group()
		except AttributeError:
			weight = "NA"
		trainer = row[2].text.strip()
	
		awt.append([age, weight, trainer])

	return awt

def get_or_ts_jockey(soup):
	otj = list()
	tbl = soup.select("table tbody tr td.lightGray")
	tbls = [tbl[j:j + 3] for j in xrange(0, len(tbl), 3)]
	for row in tbls:
		official_rating = row[0].text
		if official_rating == u"\u2014":
			official_rating = "NA"
		top_speed = row[1].text
		if top_speed == "*":
			top_speed = "NA"
		if row[2].a is not None:
			jockey = row[2].a.text
		else:
			jockey = row[2].text
	
		otj.append([official_rating, top_speed, jockey])

	return otj

def get_features(race):
	with open(race, "rb") as f:
		page = f.read()

	soup = BeautifulSoup(page, "html.parser")

	racecourse = get_racecourse(soup)
	time = get_time(soup)
	dist_going = get_dist_going(soup)
	position = get_position(soup)
	name = get_name(soup)
	country_sp = get_country_sp(soup)
	age_weight_trainer = get_age_weight_trainer(soup)
	or_ts_jockey = get_or_ts_jockey(soup)

	return {"racecourse": racecourse, "time": time, "distance": dist_going["dist"],
	"going": dist_going["ground"] , "position": position, "name": name, 
	"country": country_sp["country"], "sp": country_sp["sp"], "age_weight_trainer": age_weight_trainer,
	"or_ts_jockey": or_ts_jockey}

def get_records(race):
	horses = list()
	for i in range(len(race["name"])):
		horses.append({"racecourse": race["racecourse"], "time": race["time"], 
			"distance": race["distance"], "going": race["going"], "position": race["position"][i],
			"name": race["name"][i], "country": race["country"][i], "sp": race["sp"][i],
			"age": race["age_weight_trainer"][i][0], "weight": race["age_weight_trainer"][i][1],
			"trainer": race["age_weight_trainer"][i][2], "or": race["or_ts_jockey"][i][0],
			"ts": race["or_ts_jockey"][i][1], "jockey": race["or_ts_jockey"][i][2]})

	return horses

for j in valid:
	with open("horses.json", "a") as f:

		try:
			RACE = "Raw_HTML/" + str(j) + ".txt"
			race = get_features(RACE)
			# print get_records(race)
			for i in range(len(race["name"])):
				json.dump({"racecourse": race["racecourse"], "time": race["time"], 
				"distance": race["distance"], "going": race["going"], "position": race["position"][i],
				"name": race["name"][i], "country": race["country"][i], "sp": race["sp"][i],
				"age": race["age_weight_trainer"][i][0], "weight": race["age_weight_trainer"][i][1],
				"trainer": race["age_weight_trainer"][i][2], "or": race["or_ts_jockey"][i][0],
				"ts": race["or_ts_jockey"][i][1], "jockey": race["or_ts_jockey"][i][2]}, f)
				f.write("\n")
			print j


		except Exception as e:
			print "#ERROR:", e, j
