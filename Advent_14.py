import numpy as np

def advent_14(input_number, output_recipes, part2input=0, part1=True):
	circle = [int(i) for i in str(input_number)]
	elf1 = 0
	elf2 = 1
	j = 0
	while len(circle) < output_recipes + 11 if part1 else True:
		if not part1 and j%1000000 == 0:
			print j
		#Combine recipes
		combine = circle[elf1] + circle[elf2]
		new_recipes = [int(i) for i in str(combine)]
		circle.extend(new_recipes)
		#Choose new current recipe (indexes)
		elf1 = (elf1 + (1 + circle[elf1])) % len(circle)
		elf2 = (elf2 + (1 + circle[elf2])) % len(circle)
		if not part1:
			if len(circle) > len(part2input):
				try:
					found = np.array(circle[-2*len(part2input):]).tostring().index(np.array(part2input).tostring())
					circle_str = ''.join(str(n) for n in circle)
					input2 = ''.join(str(n) for n in part2input)
					i = circle_str.find(input2)
					return len(circle_str[:i])
				except ValueError:
					pass
		j += 1
	if part1:
		return ''.join(str(n) for n in circle[output_recipes:output_recipes+10])
		

advent_14(37, 209231)
#advent_14(37, 18)
advent_14(37, 209231,[2,0,9,2,3,1],False)

