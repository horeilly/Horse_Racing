
@outputSchema('edge_bag:bag{edge:tuple(winner:chararray, loser:chararray, weight:int)}')
def get_edges(race):
#:params: race (list), bag in pig
#:returns: ranks (list), contains tuples with (horse1, horse2, 1) where horse 1
#                        is a horse which beat horse2
    try:
        ranks = list()
        for horse in race:
            for opponent in race:
                if int(horse[5]) < int(opponent[5]):
                    ranks.append((horse[4], opponent[4], 1))
        if len(ranks) == 0:
            ranks.append(('nobody','won',-999))
        return ranks
    except:
        return [('had','error',999)]


