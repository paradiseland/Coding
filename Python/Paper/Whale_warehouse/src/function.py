
"""
define some useful function mainly about randomly storage.
"""
def get_closest_PSB(fleet, place):
    dis = float('inf')
    for i in fleet:
        if i.state == 1:
            if place[0] - i.index < dis:
                chosen = i.index
    return chosen


def reshuffle(warehouse, place, product):
    tmp = 0
    out = []
    while tmp != product:
        pop_item = warehouse.record[place[0]][place[1]].pop()
        out.append(pop_item)
        tmp = pop_item
    return out


