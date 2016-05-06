import csv
import re


horses = list()
with open("horses.csv", "rb") as horse_csv:
    horsereader = csv.reader(horse_csv, delimiter=",")
    for row in horsereader:
        horses.append(row)

print "...HORSES LOADED..."


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

for horse in horses[1:]:
    try:
        int(horse[6])
        horse[:] = [horse[0] + " " + parse_time(horse[1])] + horse[2:4] + [parse_dist(horse[4])] + \
                   horse[5:9] + [parse_weight(horse[9])] + horse[10:-1]
        i += 1
        print i

    except (ValueError, IndexError) as e:
        horses.remove(horse)
        if e == IndexError:
            print "#ERROR:", horse


j = 0

with open("parsed_horses.csv", "wb") as parsed_horses:
    horsewriter = csv.writer(parsed_horses, delimiter=",")
    horsewriter.writerow(["DateTime", horses[0][2], horses[0][3], horses[0][4], horses[0][5], horses[0][6],
                          horses[0][7], horses[0][8], horses[0][9], horses[0][10], horses[0][11], horses[0][12]])
    for horse in horses[1:]:
        try:
            horsewriter.writerow([field for field in horse])
            j += 1
            print j
        except IndexError:
            print "#ERROR:", [field for field in horse]


