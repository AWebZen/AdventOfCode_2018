import numpy as np

input_rules = [".#### => .", ".###. => .", "#.... => .", "##### => .", "..### => #", "####. => #", "..#.. => .", "###.# => .", "..##. => .", "#.##. => #", "#.#.. => .", "##... => .", "..#.# => #", "#.### => #", ".#..# => .", "#...# => #", ".##.# => #", ".#.#. => #", "#..#. => #", "###.. => #", "...#. => .", ".#.## => #", ".##.. => .", "#..## => .", "##.## => .", ".#... => #", "#.#.# => .", "##..# => .", "....# => .", "..... => .", "...## => #", "##.#. => ."]


rules = {}

for r in input_rules:
	r = r.split(" => ")
	rules[r[0]] = r[1]



pots = "#.#..#.##.#..#.#..##.######...####.........#..##...####.#.###......#.#.##..#.#.###.#..#.#.####....##"


current_0 = 0

for gen in xrange(1,21):
	if gen%1000000 == 0:
		print gen
	start_index = pots.find("#")
	if start_index == -1:
		break
	if start_index > -1 and start_index < 4: #add pots when missing for motif
		pots = "." * (4 - start_index) + pots
		current_0 += (4 - start_index)
	if start_index > -1 and start_index > 4:
		pots = pots[start_index-4:]
		current_0 -= (start_index - 4)
	end_index_rev = pots[::-1].find("#")
	if end_index_rev > -1 and end_index_rev < 4: #add pots when missing for motif
		pots += "." * (4 - end_index_rev)
	if end_index_rev > -1 and end_index_rev > 4:
		pots = pots[:-(end_index_rev-4)]
	new_pots = ".."
	for i in xrange(2, len(pots)-2):
		motif = pots[i-2:i+3]
		new_pots += rules.get(motif, ".")
	new_pots += ".."
	pots = new_pots

count_pots = 0
for p, pot in enumerate(new_pots):
	if pot == "#":
		count_pots += p - current_0

print count_pots


#Part 2


pots = "#.#..#.##.#..#.#..##.######...####.........#..##...####.#.###......#.#.##..#.#.###.#..#.#.####....##"


pots_gens = [pots]
current_0 = 0
old_0 = -1

for gen in xrange(1,50000000001):
	print current_0, gen, len(pots)
	old_0 = current_0
	start_index = pots.find("#")
	if start_index == -1:
		break
	if start_index > -1 and start_index < 4: #add pots when missing for motif
		print "in"
		pots = "." * (4 - start_index) + pots
		current_0 += (4 - start_index)
	if start_index > -1 and start_index > 4:
		pots = pots[start_index-4:]
		current_0 -= (start_index - 4)
	end_index_rev = pots[::-1].find("#")
	if end_index_rev > -1 and end_index_rev < 4: #add pots when missing for motif
		print "in2"
		pots += "." * (4 - end_index_rev)
	if end_index_rev > -1 and end_index_rev > 4:
		pots = pots[:-(end_index_rev-4)]
	print len(pots)
	new_pots = ".."
	for i in xrange(2, len(pots)-2):
		motif = pots[i-2:i+3]
		new_pots += rules.get(motif, ".")
	new_pots += ".."
	pots = new_pots
	dupli = False
	if pots in pots_gens: #Look for convergence
		pots_gens.append(new_pots)
		dzeros = current_0 - old_0
		fiftybillion_0 = current_0 + (50000000000 - gen) * dzeros
		break
	pots_gens.append(new_pots)


count_pots = 0
for p, pot in enumerate(new_pots):
	if pot == "#":
		count_pots += p - fiftybillion_0

print count_pots
