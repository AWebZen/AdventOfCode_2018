def get_scores(players, marbl_num):
	scores = {p:0 for p in range(1, players+1)}
	player = 3
	marbles = [0,1]
	i_curr = 1
	for marbl in xrange(2, marbl_num + 1):
		if marbl < 2647 and marbl > 2644:
			#print player, marbles, scores
			print player, marbl, scores, i_curr, marbles[i_curr], marbles[i_curr-7:i_curr]
			print marbles
		if marbl < 2625 and marbl > 2621:
			#print player, marbles, scores
			print player, marbl, scores, i_curr, marbles[i_curr], marbles[i_curr-7:i_curr]
			print marbles
		if marbl > 93 and 93 not in marbles:
			print 93, marbl
			break
		if marbl % 23 == 0:
		  	scores[player] += marbl + marbles[i_curr-7]
		  	del marbles[i_curr-7]
		  	i_curr -= 7
		else:
			i_curr += 2
			if i_curr == len(marbles):
				marbles.append(marbl)
			else:
				if i_curr > len(marbles):
					i_curr -= len(marbles)
				marbles = marbles[:i_curr] + [marbl] + marbles[i_curr:]
		player += 1
		if player > players:
			player = 1
	return scores



from collections import deque, defaultdict
from itertools import cycle

def run_game(_max_marble, _player_count):
    elves = defaultdict(int)
    circle = deque()
    for current_marble, current_elf in zip(range(_max_marble+1), cycle(range(1,_player_count+1))):
	if current_marble > 2644 and current_marble < 2647:
		#print current_elf, circle, elves
		print current_marble, current_elf, elves
	if current_marble > 2621 and current_marble < 2625:
		#print current_elf, circle, elves
		print current_marble, current_elf, elves
	if current_marble > 38 and 38 not in circle:
		print current_marble
		break
        if current_marble and current_marble % 23 == 0:
            circle.rotate(7)
	    if current_marble > 2644 and current_marble < 2647:
	        print circle
	    if current_marble > 2621 and current_marble < 2625:
	        print circle
            elves[current_elf] += current_marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(current_marble)
    return elves

sc = get_scores(13, 7999)
sc2 = run_game(7999, 13)
#sc = get_scores(439, 71307)
#sc = get_scores(9, 25)

print [(i,v) for i,v in sc.items() if v == max(sc.values())]
print [(i,v) for i,v in sc2.items() if v == max(sc2.values())]
