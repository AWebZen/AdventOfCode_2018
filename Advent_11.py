import numpy as np

serial = 5468

def power_fuel(serial, coords = False):
	X = np.zeros((300,300))
	Y = np.zeros((300,300))
	for i in range(1,300+1):
		X[i-1,:] = i
		Y[:,i-1] = i
	rackID = X+10
	power = np.zeros((300,300))
	for i in range(300):
		for j in range(300):
			power[i,j] = int(str(int((rackID[i,j] * Y[i,j] + serial) * rackID[i,j]))[-3]) - 5
	if coords:
		print power[coords[0]-1, coords[1]-1]
	return power

power = power_fuel(57, [122,79])
power = power_fuel(39, [217,196])
power = power_fuel(71, [101,153])
power = power_fuel(18, [33,45])

power = power_fuel(5468)

def largest_power(power, size):
	power_3x3 = np.zeros((300-size+1,300-size+1))
	for i in range(300-size+1):
		for j in range(300-size+1):
			power_3x3[i,j] = np.sum(power[i:i+size,j:j+size])
	return np.array(np.unravel_index(np.argmax(power_3x3), power_3x3.shape))+1, np.max(power_3x3)

print largest_power(power, 3)
		
#Part 2

def largest_power_sizes(power):
	maxes = []
	max_ind = []
	for size in range(1,301):
		print size
		ind, mxx = largest_power(power, size)
		maxes.append(mxx)
		max_ind.append(ind)
	return np.argmax(maxes)+1, max_ind[np.argmax(maxes)], np.max(maxes)

print largest_power_sizes(power)
	


