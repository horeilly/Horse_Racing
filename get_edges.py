import csv
from pprint import pprint

def get_edges_json(race):
    ranks = dict()
    for horse in race:
        for opponent in race:
            try:
                if int(horse[5]) < int(opponent[5]):
                    ranks[horse[4]][opponent[4]] = 1
                else:
                    ranks[horse[4]][opponent[4]] = 0
            except KeyError:
                ranks[horse[4]] = dict()
                if int(horse[5]) < int(opponent[5]):
                    ranks[horse[4]][opponent[4]] = 1
                else:
                    ranks[horse[4]][opponent[4]] = 0
    return ranks


def get_edges_csv(race):
    ranks = list()
    for horse in race:
        for opponent in race:
            if int(horse[5]) < int(opponent[5]):
                ranks.append([horse[4], opponent[4], 1])
            else:
                ranks.append([horse[4], opponent[4], 0])
    return ranks


with open("toy_race.csv", "rb") as f:
    racereader = csv.reader(f)
    race = [tuple(horse) for horse in racereader]


pprint(who_beats_who_csv(race))
