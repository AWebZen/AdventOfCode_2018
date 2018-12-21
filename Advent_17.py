#Not very quick
import numpy as np

def output_print(grid):
    """Prints grid"""
    x, y = grid.shape
    for i in range(x):
        for j in range(y):
            print grid[i, j],
        print

def read_input(fname="Advent_17_input.txt"):
    """Parses input to get array of coordinates"""
    coordinates = []
    with open(fname, "r") as f:
        for coord in f:
            coord = coord.rstrip("\n")
            coord = coord.split(", ")
            coord1 = coord[0].split("=")
            if coord1[0] == "y":
                x = int(coord1[1])
                y = False
            else:
                x = False
                y = int(coord1[1])
            coord2 = coord[1][2:].split("..")
            if x:
                coordinates.extend([[x, yi] for yi in xrange(int(coord2[0]), int(coord2[1])+1)])
            else:
                coordinates.extend([[xi, y] for xi in xrange(int(coord2[0]), int(coord2[1])+1)])
    coordinates = np.array(coordinates)
    return coordinates


def build_grid(water_spring, fname="Advent_17_input.txt"):
    """Builds grid with clay, soil, and the water spring"""
    coordinates = read_input(fname)
    max_coords = np.max(coordinates, axis=0)
    min_coords = np.min(coordinates, axis=0)
    grid = np.full((max_coords[0]+1, max_coords[1]+1+10 - (min_coords[1]-10)), ".") #added 10 on each side for y, to let water run if needed (their x)
    y_left = min_coords[1]-10
    water_spring[1] -= y_left
    grid[water_spring[0], water_spring[1]] = "+"
    coordinates[:, 1] -= y_left
    for c in coordinates:
        x, y = c
        grid[x, y] = "#"
    return grid, max_coords, min_coords, water_spring


def flow(grid, water_spring):
    """Let water flow from water spring"""
    down = [water_spring]
    step = 0
    # TODO - add source when stagnant water at x_above, and popleft of deque to stop while
    while step < 10: #Stop when 10 streams of water go out of range
        for i in xrange(len(down)):
            try:
                current_x, current_y = down[i]
                while grid[current_x+1, current_y] not in ["~", "#"]: #Down we go - the fall
                    grid[current_x+1, current_y] = "|"
                    current_x += 1
                #Left and right we go
                current_y_l = current_y
                current_y_r = current_y
                right = True
                left = True
                while left:
                    if grid[current_x, current_y_l-1] not in ["#"]: #left
                        grid[current_x, current_y_l-1] = "|"
                        current_y_l -= 1
                        if grid[current_x+1, current_y_l] not in ["~", "#"]: #Can left water fall?
                            if [current_x, current_y_l] not in down:
                                down.append([current_x, current_y_l]) #New falling source!
                            break
                    else:
                        left = False
                while right:
                    if grid[current_x, current_y_r+1] not in ["#"]: #right
                        grid[current_x, current_y_r+1] = "|"
                        current_y_r += 1
                        if grid[current_x+1, current_y_r] not in ["~", "#"]: #Can right water fall?
                            if [current_x, current_y_r] not in down:
                                down.append([current_x, current_y_r]) #New falling source!
                            break
                    else:
                        right = False
                if not right and not left: #Stagnant water
                    grid[current_x, current_y_l:current_y_r+1] = "~"
            except IndexError:
                step += 1
    return grid


grid, max_coords, min_coords, water_spring = build_grid([0, 500], fname="Advent_17_input.txt")
grid = flow(grid, water_spring)

#Part 1 - should we count the water source? (not applicable in example)
print np.sum(np.in1d(grid[min_coords[0]:max_coords[0]+1, :], ["|", "~", "+"])) 
print np.sum(grid[min_coords[0]:max_coords[0]+1, :] == "~") #Part 2
