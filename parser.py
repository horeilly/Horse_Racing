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


def html(page):
    with open(page, "rb") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")

    return soup


more_than_one = list()

for i in valid:
    try:
        # RACECOURSE ROBUST
        # header = html("Raw_HTML/" + str(i) + ".txt").title.text.split(" | ")
        # print re.sub(r"Results From The (\d\.|\d\d\.)\d\d Race At ", "",
        # header[0]), i

        # TIME ROBUST
        # var = html("Raw_HTML/" + str(i) + ".txt").find("div",
        # 	{"class": "leftColBig"}).find("span",
        # 	{"class": "timeNavigation"}).text
        # print re.search(r"(\d\d|\d):\d\d", var).group(), i

        # POSITION ROBUST
        # var = html("Raw_HTML/" + str(i) + ".txt")
        # positions = [item.text.strip() for item in
        #              var.find_all("td", {"class": "nowrap noPad"})]
        # if len(positions) > 1:
        #     more_than_one.append(i)

        # HORSE NAME ROBUST
        # var = html("Raw_HTML/" + str(i) + ".txt")
        # v2 = [item.text for item in var.find_all("a", {"title":
        # 	"Full details about this HORSE"})]

        # NAME, COUNTRY, SP ROBUST
        # var = html("Raw_HTML/" + str(i) + ".txt")
        # v3 = [item.text.strip().split("\n ") for item in
        #       var.find_all("span", {"class": "black"})]

        # v4 = [re.search(r"\d+-\d+", item.span.text).group() for item in \
        # var.find_all("td", {"class": "nowrap black"}) if
        # item.span is not None]


        with open("name_sp_country.json", "a") as f:
            json.dump(out, f)
            f.write("\n")

        # print v4

    except Exception as e:
        print e, i

# print more_than_one
#
# with open("more_than_one.txt", "wb") as f:
#     for i in more_than_one:
#         f.write(str(i) + "\n")
