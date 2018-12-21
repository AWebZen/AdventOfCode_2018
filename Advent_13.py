import numpy as np
from copy import deepcopy

rails = []
with open("Advent_13_input.txt", "r") as f:
	for line in f:
		line = line.rstrip("\n")
		rails.append(list(line))

rails = np.array(rails)


intersection = {"l":"s", "s":"r", "r":"l"}

new_dir_intersection = {"l":{"<":"v", ">":"^", "^":"<", "v":">"}, 
	"s":{"<":"<", ">":">", "^":"^", "v":"v"},
	"r":{"<":"^", ">":"v", "^":">", "v":"<"},
	}

def get_new_coords (i,j, dirc):
	return {"<": [i,j-1],
	">":[i,j+1], 
	"^":[i-1,j], 
	"v":[i+1,j],
	}[dirc]

def get_order_carts(wagons): #loop on carts from top to bottom, left to right
	coords = []
	for w in sorted(wagons.keys()):
		coords.append(list(wagons[w][0])+[w])
	coords = np.array(coords)
	new_sort = np.argsort(coords[:,0])
	return np.array(coords)[new_sort,2]
	

def get_new_direction(dirc, curve):
	return {"/" : {"^":">", "<":"v",">":"^","v":"<",},
		"\\" : {"^":"<", "v":">", "<":"^", ">":"v",}
		}[curve][dirc]


def next_step(wag, rails, new_dir_intersection,no_wags_rails):
	#print wag, rails[wag[0][0],wag[0][1]]
	i,j = get_new_coords(wag[0][0],wag[0][1], wag[1])
	next_step = rails[i,j]
	i_old, j_old = wag[0][0],wag[0][1]
	wag[0] = np.array([i,j])
	if next_step == "/" or next_step == "\\":
		wag[1] = get_new_direction(wag[1], next_step)
	elif next_step == "+":
		wag[1] = new_dir_intersection[wag[2]][wag[1]]
		wag[2] = intersection[wag[2]]
	elif next_step in ["<", ">", "^", "v"]:
		rails[i_old,j_old] = no_wags_rails[i_old,j_old]
		rails[i,j] = no_wags_rails[i,j]
		return wag[0], rails
	#print wag, rails[i,j], wag[1]
	rails[i_old,j_old] = no_wags_rails[i_old,j_old]
	rails[i,j] = wag[1]
	return wag, rails
		

wagons = {}
wag_counter = 0
for direction in ["<", ">", "^", "v"]:
	wags = np.array(np.where(rails == direction)).T
	for w in wags:
		wagons[wag_counter] = [w, direction, "l"]
		wag_counter += 1


no_wags_rails = deepcopy(rails)
for w, wag in wagons.items():
	i,j = wag[0]
	if wag[1] in [">","<"]:
		actual_sign = "-"
	else:
		actual_sign = "|"
	no_wags_rails[i,j] = actual_sign

def part1 (wagons, rails, new_dir_intersection, no_wags_rails):
	while True:
		order_carts = get_order_carts(wagons)
		for w in order_carts:
			wag = wagons[w]
			wagons[w], rails = next_step(wag, rails, new_dir_intersection, no_wags_rails)
			if len(wagons[w]) == 2:
				break
		if len(wagons[w]) == 2:
			print wagons[w][1], wagons[w][0] #Inverted axis in text
			break

#part1(wagons, rails, new_dir_intersection, no_wags_rails)



#PART 2
step = 0
while len(wagons) > 1:
	order_carts = get_order_carts(wagons)
	for w in order_carts:
		if w not in wagons.keys():
			continue
		wag = wagons[w]
		stop = False
		if len(wagons)%2 == 0:
			stop=True
			break
		wagons[w], rails = next_step(wag, rails, new_dir_intersection, no_wags_rails)
		if len(wagons[w]) == 2:
			coords_remove = wagons[w]
			del wagons[w]
			for w, wag in wagons.items():
				if wag[0][0] == coords_remove[0] and wag[0][1] == coords_remove[1]:
					del wagons[w]
	if stop:
		break
	step += 1

print wagons.values()[0][0][1], wagons.values()[0][0][0]

