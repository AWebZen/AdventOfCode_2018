import networkx as nx
import numpy as np


orders_all = ['Step G must be finished before step N can begin.', 'Step N must be finished before step B can begin.', 'Step P must be finished before step Q can begin.', 'Step F must be finished before step U can begin.', 'Step H must be finished before step A can begin.', 'Step C must be finished before step S can begin.', 'Step A must be finished before step K can begin.', 'Step M must be finished before step O can begin.', 'Step V must be finished before step L can begin.', 'Step E must be finished before step L can begin.', 'Step B must be finished before step Q can begin.', 'Step W must be finished before step J can begin.', 'Step R must be finished before step D can begin.', 'Step D must be finished before step S can begin.', 'Step S must be finished before step X can begin.', 'Step Q must be finished before step J can begin.', 'Step I must be finished before step L can begin.', 'Step U must be finished before step J can begin.', 'Step Z must be finished before step X can begin.', 'Step Y must be finished before step T can begin.', 'Step J must be finished before step K can begin.', 'Step T must be finished before step L can begin.', 'Step K must be finished before step O can begin.', 'Step O must be finished before step X can begin.', 'Step L must be finished before step X can begin.', 'Step Y must be finished before step O can begin.', 'Step F must be finished before step S can begin.', 'Step K must be finished before step L can begin.', 'Step Z must be finished before step O can begin.', 'Step J must be finished before step X can begin.', 'Step K must be finished before step X can begin.', 'Step Q must be finished before step X can begin.', 'Step Y must be finished before step L can begin.', 'Step E must be finished before step S can begin.', 'Step H must be finished before step Y can begin.', 'Step G must be finished before step P can begin.', 'Step E must be finished before step K can begin.', 'Step B must be finished before step L can begin.', 'Step T must be finished before step K can begin.', 'Step N must be finished before step R can begin.', 'Step F must be finished before step E can begin.', 'Step W must be finished before step Y can begin.', 'Step U must be finished before step X can begin.', 'Step A must be finished before step I can begin.', 'Step Q must be finished before step Y can begin.', 'Step P must be finished before step T can begin.', 'Step D must be finished before step X can begin.', 'Step E must be finished before step Y can begin.', 'Step F must be finished before step B can begin.', 'Step P must be finished before step I can begin.', 'Step N must be finished before step S can begin.', 'Step F must be finished before step V can begin.', 'Step W must be finished before step U can begin.', 'Step F must be finished before step A can begin.', 'Step I must be finished before step Z can begin.', 'Step E must be finished before step D can begin.', 'Step R must be finished before step I can begin.', 'Step M must be finished before step V can begin.', 'Step R must be finished before step U can begin.', 'Step R must be finished before step X can begin.', 'Step G must be finished before step O can begin.', 'Step G must be finished before step H can begin.', 'Step M must be finished before step R can begin.', 'Step E must be finished before step U can begin.', 'Step F must be finished before step Z can begin.', 'Step N must be finished before step Q can begin.', 'Step U must be finished before step O can begin.', 'Step J must be finished before step T can begin.', 'Step W must be finished before step Z can begin.', 'Step I must be finished before step J can begin.', 'Step U must be finished before step L can begin.', 'Step I must be finished before step X can begin.', 'Step Z must be finished before step J can begin.', 'Step F must be finished before step D can begin.', 'Step N must be finished before step O can begin.', 'Step Q must be finished before step U can begin.', 'Step G must be finished before step L can begin.', 'Step H must be finished before step Q can begin.', 'Step M must be finished before step Q can begin.', 'Step N must be finished before step D can begin.', 'Step Z must be finished before step L can begin.', 'Step I must be finished before step Y can begin.', 'Step E must be finished before step X can begin.', 'Step J must be finished before step L can begin.', 'Step H must be finished before step W can begin.', 'Step P must be finished before step Y can begin.', 'Step Q must be finished before step T can begin.', 'Step Z must be finished before step Y can begin.', 'Step R must be finished before step T can begin.', 'Step E must be finished before step J can begin.', 'Step I must be finished before step T can begin.', 'Step A must be finished before step L can begin.', 'Step E must be finished before step R can begin.', 'Step T must be finished before step O can begin.', 'Step Y must be finished before step X can begin.', 'Step A must be finished before step Q can begin.', 'Step W must be finished before step Q can begin.', 'Step A must be finished before step T can begin.', 'Step B must be finished before step Y can begin.', 'Step H must be finished before step E can begin.', 'Step H must be finished before step K can begin.']


g = nx.DiGraph()

for order in orders_all:
	order = order.lower().split("step ")
	g.add_edge(order[1][0].upper(), order[2][0].upper())


origins = sorted([v for v, d in g.in_degree() if d == 0])

#STEP 1
right_order = []
tasks = origins[:]
i = 0
while tasks:
	if len(list(g.predecessors(tasks[i]))) == 0 or np.all(np.in1d(list(g.predecessors(tasks[i])), right_order)): #Available letter/task
		tsk = tasks.pop(i)
		right_order.append(tsk)
		downstream_tasks = list(g.successors(tsk))
		tasks += [down_t for down_t in downstream_tasks if down_t not in tasks and down_t not in right_order]
		tasks = sorted(tasks)
		i = 0
	else:
		i += 1

print "".join(right_order)



#STEP 2

abc_time = {a:i+60+1 for i, a in enumerate(sorted(g.nodes))}

tasks_done = []
currently = origins + [-10]
current_t0 = [0 for i in range(len(origins))] + [-10]
available_tasks = []
time = 0
while len(tasks_done) < len(g.nodes):
	time += 1
	for i_task, task in enumerate(currently):
		if current_t0[i_task] != -10 and current_t0[i_task] == time - abc_time.get(task, False):
			tasks_done.append(task)
			downstream_tasks = list(g.successors(task))
			available_tasks += [down_t for down_t in downstream_tasks if down_t not in available_tasks and down_t not in tasks_done and down_t not in currently] #add available successors
			available_tasks = sorted(available_tasks)
			currently[i_task] = -10
			current_t0[i_task] = -10
			#print len(tasks_done)
	for worker in range(5):
		if current_t0[worker] != -10:
			continue
		letter = False
		i_curr = 0
		while not letter and i_curr < len(available_tasks): #Try to find available letter
			letter = available_tasks[i_curr]
			if len(list(g.predecessors(letter))) == 0 or np.all(np.in1d(list(g.predecessors(letter)), tasks_done)) : #Letter has available predecessors and is not in use (predecessors in tasks_done and not in current)
				currently[worker] = letter
				current_t0[worker] = time
				del available_tasks[i_curr]
				#print time, currently, current_t0, available_tasks
			else:
				letter = False
				i_curr += 1

print time, "seconds needed"


