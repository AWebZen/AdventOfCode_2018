import numpy as np
from copy import deepcopy

"""
^, v, >, < : cart directions
l, s, r: left, straight, right turns at intersections.
"""
    
def get_rails_wagons(fname="Advent_13_input.txt"):
    """Get railway and wagons from input"""
    # Rails with wagons
    rails = []
    with open(fname, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            rails.append(list(line))
    
    rails = np.array(rails)

    # Wagons definition
    wagons = {} # {id:[coords, direction, future intersection behaviour]}
    wag_counter = 0
    for direction in ["<", ">", "^", "v"]:
        wags = np.array(np.where(rails == direction)).T
        for w in wags:
            wagons[wag_counter] = [list(w), direction, "l"]
            wag_counter += 1
    
    # Removal of wagons from rails
    no_wags_rails = deepcopy(rails)
    #On initial map, track under cart is a straight path in the cart direction
    for w, wag in wagons.items():
        i,j = wag[0]
        if wag[1] in [">","<"]:
            actual_sign = "-"
        else:
            actual_sign = "|"
        no_wags_rails[i,j] = actual_sign
    return no_wags_rails, wagons


def get_new_coords (i, j, dirc):
    """New coordinates depending on cart direction"""
    return {"<":[i,j-1],
            ">":[i,j+1], 
            "^":[i-1,j], 
            "v":[i+1,j],
            }[dirc]


def get_order_carts(wagons): 
    """Carts/wagons move in reading-order:left to right, top to down"""
    coords = []
    for w in sorted(wagons.keys()):
        coords.append(list(wagons[w][0]) + [w])
    coords = np.array(coords)
    new_sort = np.argsort(coords[:,0])
    return np.array(coords)[new_sort,2]
    

def get_new_direction(dirc, curve):
    """Direction change after curve"""
    return {"/" : {"^":">", "<":"v",">":"^","v":"<",},
        "\\" : {"^":"<", "v":">", "<":"^", ">":"v",}
        }[curve][dirc]


def next_step(wag, wagons, no_wags_rails):
    """
    Our cart takes a step
    
    Parameters
    -------
    wag - wagon defined by [coords, direction, future intersection behaviour]
    no_wags_rails - numpy array of the rail grid without carts
    
    Returns
    -------
    wag - wagon defined by [new coords, new direction, future intersection behaviour]
    no_wags_rails - numpy array of the rail grid without carts
    """
    #Our cart moves...
    i_old, j_old = wag[0][0], wag[0][1]
    i, j = get_new_coords(i_old, j_old, wag[1])
    nxt_step = no_wags_rails[i,j]
    
    #What does it find?
    if [i,j] in [wagn[0] for w, wagn in wagons.items()]: #collision
        return [i,j], no_wags_rails
    
    elif nxt_step == "/" or nxt_step == "\\": #curve
        wag[1] = get_new_direction(wag[1], nxt_step)
        
    elif nxt_step == "+": #intersection
        wag[1] = NEW_DIR_INTERSECTION[wag[2]][wag[1]]
        wag[2] = INTERSECTION[wag[2]]
    
    #straight path
    wag[0] = [i,j] #updating coordinates
    return wag, no_wags_rails
        

def part1 (wagons, no_wags_rails):
    """
    Find coordinates of first collision
    """
    while True:
        order_carts = get_order_carts(wagons)
        for w in order_carts:
            wag = wagons[w]
            wagons[w], no_wags_rails = next_step(wag, wagons, no_wags_rails)
            if len(wagons[w]) == 2:
                break
        if len(wagons[w]) == 2:
            print "Part 1"
            print "Location of first crash: {}, {}".format(wagons[w][1], wagons[w][0]) #Inverted axis in text
            break


def part2 (wagons, no_wags_rails):
    """Where will the last cart that hasn't crashed end up?"""
    step = 0
    while len(wagons) > 1:
        order_carts = get_order_carts(wagons)
        for w in order_carts:
            if w not in wagons.keys():
                continue
            wag = wagons[w]
            stop = False
            if len(wagons)%2 == 0: #Not a single cart alive
                stop = True
                break
            wagons[w], no_wags_rails = next_step(wag, wagons, no_wags_rails)
            if len(wagons[w]) == 2:
                coords_remove = wagons[w]
                del wagons[w]
                for w, wag in wagons.items():
                    if wag[0][0] == coords_remove[0] and wag[0][1] == coords_remove[1]:
                        del wagons[w]
        if stop:
            break
        step += 1
    print "Part 2"
    print "Location of last cart: {}, {}".format(wagons.values()[0][0][1], wagons.values()[0][0][0]) #Inverted axis in text
    

#Looping on intersection behaviour
INTERSECTION = {"l":"s", "s":"r", "r":"l"}

#New direction after intersection, depending on behaviour
NEW_DIR_INTERSECTION = {"l": {"<":"v", ">":"^", "^":"<", "v":">"}, 
                        "s": {"<":"<", ">":">", "^":"^", "v":"v"},
                        "r": {"<":"^", ">":"v", "^":">", "v":"<"},
                        }


if __name__ == '__main__':
    #Part 1
    no_wags_rails, wagons = get_rails_wagons()
    part1(wagons, no_wags_rails)
    
    print
    
    #Part 2
    no_wags_rails, wagons = get_rails_wagons()
    part2 (wagons, no_wags_rails)

