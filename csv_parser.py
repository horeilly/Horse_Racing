import csv
import re
from datetime import datetime


def parse_date(date):
    return datetime.strptime(date, "%d %B %Y").strftime("%Y-%m-%d")


def parse_time(time):
    if int(time.split(":")[0]) < 11:
        return str(int(time.split(":")[0]) + 12) + ":" + time.split(":")[1] + ":00"
    else:
        return str(int(time.split(":")[0])) + ":" + time.split(":")[1] + ":00"


def parse_dist(a):
    m, f, y = 1, 1./8, 1./1760
    splitchars = re.sub('([mfy])', ' \\1 ', a).split(' ')[0:-1]
    return round(sum([eval('*'.join(splitchars[i:i+2])) for i in range(0, len(splitchars), 2)]), 3)


def parse_weight(weight):
    try:
        weight = weight.split("-")
        if int(weight[1]) > 13:
            return round(int(weight[0]) + float("".join(list(weight[1])[0:-1])) / 14, 2)
        else:
            return round(int(weight[0]) + float(weight[1]) / 14, 2)
    except ValueError:
        return "NA"


i = 0
with open("unparsed_horses.csv", "rb") as unparsed_horse_csv:
    with open("horses2.csv", "wb") as horses:

        horsereader = csv.reader(unparsed_horse_csv, delimiter=",")
        horsewriter = csv.writer(horses, delimiter=",")

        horsewriter.writerow(["DateTime", "Racecourse", "Ground", "Distance", "Horse", "Position", "Jockey", "Trainer", 
            "Weight", "Age", "Country", "OR"])
        horsereader.next()

        for row in horsereader:
            try:
                int(row[6])
                horse = [parse_date(row[0]) + " " + parse_time(row[1])] + row[2:4] + [parse_dist(row[4])] + row[5:9] + \
                [parse_weight(row[9])] + row[10:-1]
                horsewriter.writerow(horse)

                i += 1
                print i

            except (ValueError, IndexError) as e:
                pass
