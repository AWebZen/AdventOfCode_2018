import networkx as nx
import numpy as np
from copy import deepcopy
from collections import defaultdict

def parse_output(fi):
    grid = []
    with open(fi, "r") as f:
        for line in f:
            grid.append(list(line.rstrip("\n")))
    return np.array(grid)


def from_grid_to_graph(grid):
    g = nx.Graph()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell in ["G", "E", "."]:
                g.add_node(str(i)+"-"+str(j))
                if i+1 < len(grid) and grid[i+1,j] in ["G", "E", "."]:
                    g.add_edge(str(i)+"-"+str(j), str(i+1)+"-"+str(j))
                if j+1 < len(grid[0]) and grid[i,j+1] in ["G", "E", "."]:
                    g.add_edge(str(i)+"-"+str(j), str(i)+"-"+str(j+1))
    return g



def in_range_positions(you_coords, enemy, grid, units):
    assert enemy in ["E", "G"], "Who are you?"
    x,y = you_coords
    if enemy in [grid[x-1,y], grid[x,y-1], grid[x,y+1], grid[x+1,y]]:
        return [[x,y]]
    in_range = []
    for i, j in sorted(units[enemy].keys()):
        if grid[i-1,j] == ".":
            in_range.append([i-1,j])
        if grid[i+1,j] == ".":
            in_range.append([i+1,j])
        if grid[i,j-1] == ".":
            in_range.append([i,j-1])
        if grid[i,j+1] == ".":
            in_range.append([i,j+1])
    return sorted(in_range)




def reachability_graph(you_coords, ids, g):
    g_tmp = deepcopy(g)
    
    #Removing occupied positions
    for i,j in sorted(ids.values()): #all occupied positions
        if [i,j] == list(you_coords): #Don't remove yourself
            continue
        if str(i)+"-"+str(j) in g_tmp.nodes():
            g_tmp.remove_node(str(i)+"-"+str(j))
    
    return g_tmp



def nearest_in_range(you_coords, in_range, g_tmp):
    inRange_dists = defaultdict(list)
    #Evaluating distances of in range positions
    for i,j in sorted(in_range):
        try:
            inRange_dists[nx.shortest_path_length(g_tmp, source=str(you_coords[0])+"-"+str(you_coords[1]), target=str(i)+"-"+str(j))].append([i,j])
        except: #No path, no node
            pass
    if len(inRange_dists) == 0:
        return None, None
    return min(inRange_dists.keys()), inRange_dists[min(inRange_dists.keys())][0]



def get_moving(target, you, you_coords, g_tmp, units, ids, grid):
    if target == None:
        return you_coords, units, ids, grid
    distances = nx.single_source_shortest_path_length(g_tmp, str(target[0])+"-"+str(target[1]))
    x,y = you_coords
    possible_movs = [[x-1,y], [x,y-1], [x,y], [x,y+1], [x+1,y]]
    movs_dists = [distances[str(i)+"-"+str(j)] if str(i)+"-"+str(j) in distances.keys() else max(distances.values())+1 for i,j in possible_movs]
    move = possible_movs[np.argmin(movs_dists)]
    if move != list(you_coords):
        #print "unit", you, you_coords, "moves to", move
        units[grid[x,y]][tuple(move)] = units[grid[x,y]][tuple(you_coords)]
        del units[grid[x,y]][tuple(you_coords)]
        ids[you] = tuple(move)
        grid[move[0], move[1]] = grid[x,y]
        grid[x,y] = "."
    return move, units, ids, grid



def we_attack(enemy, you, you_coords, units, ids, grid, elf_attack=3):
    x,y = you_coords
    #Do we attack?
    enem_coords = [[[x-1,y], [x,y-1], [x,y+1], [x+1,y]][i] for i in np.where(np.array([grid[x-1,y], grid[x,y-1], grid[x,y+1], grid[x+1,y]]) == enemy)[0]]
    #print "enemies!", enem_coords, you, you_coords
    if len(enem_coords) > 0:
        #Whom?
        hps = sorted([[coords, hp] for coords, hp in units[enemy].items() if list(coords) in enem_coords])
        victim = min(hps, key=lambda x:x[1])
        if enemy == "G":
            units[enemy][victim[0]] -= elf_attack
        else:
            units[enemy][victim[0]] -= 3
        #print "unit", you, you_coords, "attacks", victim[0], units
        if units[enemy][victim[0]] <= 0:
            ids = {unit:coords for unit, coords in ids.items() if coords != tuple(victim[0])}
            del units[enemy][tuple(victim[0])]
            grid[victim[0][0], victim[0][1]] = "."
    return units, ids, grid


#TODO ID individuals, since they change identity (one dies, the other one moves and therefore "usurps" identity)
#https://github.com/ShaneMcC/aoc-2018/tree/master/15/tests






def game(attack_power, grid, g, units, ids):
    stop = False
    rounds = 1
    elves = len(units["E"])
    while True : #"E" in grid and "G" in grid:
        for you, you_coords in sorted(ids.items(), key=lambda x:x[1]):
            #print you, you_coords, grid[you_coords[0], you_coords[1]]#, units#, ids.items()
            if attack_power != 3 and elves != len(units["E"]):
                print "An elf died"
                return grid, units, rounds
            if you not in ids.keys():
                continue
            if grid[you_coords[0], you_coords[1]] == "E":
                enemy = "G"
            else:
                enemy = "E"
            #print "enemy", enemy, len(units[enemy]) 
            if len(units[enemy]) == 0: #Incomplete round not counted
                stop = True
                rounds -= 1
                break
            in_range = in_range_positions(you_coords, enemy, grid, units)
            g_tmp = reachability_graph(you_coords, ids, g)
            min_dist, target = nearest_in_range(you_coords, in_range, g_tmp)
            #print "Target", min_dist, target
            new_coords, units, ids, grid = get_moving(target, you, you_coords, g_tmp, units, ids, grid)
            units, ids, grid = we_attack(enemy, you, new_coords, units, ids, grid, attack_power)
        if stop:
            break
        rounds += 1
        #print rounds, "G", sorted(units["G"]), "E", sorted(units["E"])#stop
        #print grid, units
    return grid, units, rounds




grid = parse_output("Advent_15_input.txt")

g = from_grid_to_graph(grid)

units = {
        "E" : {tuple(unit):200 for unit in np.vstack(np.where(grid == "E")).T},
        "G" : {tuple(unit):200 for unit in np.vstack(np.where(grid == "G")).T},
        }

i = 0
ids = {}
for j in units.keys():
    for coords in units[j].keys():
        ids[i] = coords
        i += 1

elves = len(units["E"])
attack_power = 3
while len(units2["E"]) != elves:
    grid2, units2, rounds = game(attack_power, grid, g, units, ids)
    #Part 1
    if attack_power == 3:
        if "G" in grid2:
            print sum(units2["G"].values())*rounds
        else:
            print sum(units2["E"].values())*rounds
    attack_power += 1


