# -*- coding: utf-8 -*-
from scipy.spatial.distance import cityblock #Manhattan distance
from collections import Counter

INPUT_DATA = [instr.split(",") for instr in open("Advent_3_2019_input.txt", "r").read().split("\n")]

#==============================================================================
# PART 1
#==============================================================================
def get_indexes(instructions):
    indx = []
    current = (0,0)
    for instr in instructions:
        dirc = instr[0]
        steps = int(instr[1:])
        if dirc == "R":
            indx += [(current[0], current[1] + i) for i in range(1, steps+1)]
        elif dirc == "L":
            indx += [(current[0], current[1] - i) for i in range(1, steps+1)]
        elif dirc == "U":
            indx += [(current[0] + i, current[1]) for i in range(1, steps+1)]
        elif dirc == "D":
            indx += [(current[0] - i, current[1]) for i in range(1, steps+1)]
        current = indx[-1]
    return indx

def intersections(indx1, indx2):
    #self-crossing does not count - removing duplicates
    indx1 = list(set(indx1))
    indx2 = list(set(indx2))
    #get intersections
    c = Counter(indx1+indx2)
    intersections = [k for k, v in c.items() if v > 1 and k != (0,0)]
    return sorted(intersections)
    
indx1 = get_indexes(INPUT_DATA[0])
indx2 = get_indexes(INPUT_DATA[1])
intersects = intersections(indx1, indx2)

dists = []
for intr in intersects:
    d = cityblock((0,0), intr)
    dists.append(d)
    
print(min(dists))

#==============================================================================
# PART 2
#==============================================================================
def steps(indx1, indx2, intersects):
    steps = []
    for intr in intersects:
        steps.append(indx1.index(intr) + 1 + indx2.index(intr) + 1)
    return steps

print(min(steps(indx1, indx2, intersects)))
    