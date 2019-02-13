import numpy as np


def power_fuel(serial, coords=False):
	"""
	Evaluate power level of each fuel cell.
    	
	Parameters
    -------
    serial - serial (puzzle input)
    coords - coordinates. If given, prints power level of given coordinates.
             Defaults to False.
             
    Returns
    -------
    power - numpy array of fuel cell power level
	"""
	X = np.zeros((300,300))
	Y = np.zeros((300,300))
	for i in range(1,300+1):
		X[i-1,:] = i
		Y[:,i-1] = i
	rackID = X+10
	power = np.zeros((300,300))
	for i in range(300):
		for j in range(300):
			try:
				power[i,j] = int(str(int((rackID[i,j] * Y[i,j] + serial) 
                                 * rackID[i,j]))[-3]) - 5
			except IndexError:
				power[i,j] = -5
	if coords:
		print power[coords[0]-1, coords[1]-1]
	return power



def largest_power(power, size):
    """
    Finds the size x size square with the largest total power. It is identified by the 
    top-left fuel cell.
    
    Parameters
    -------
    power - numpy array of fuel cell power level
    size - int, size of square
    
    Returns
    -------
    Top-left fuel cell coordinates of largest total power size x size square.
    Total power associated to square.
    """
	power_3x3 = np.zeros((300-size+1, 300-size+1))
	for i in range(300-size+1):
		for j in range(300-size+1):
			power_3x3[i,j] = np.sum(power[i:i+size,j:j+size])
	return np.array(np.unravel_index(np.argmax(power_3x3), power_3x3.shape)) + 1, np.max(power_3x3)



def largest_power_sizes(power):
    """
    Finds identifier and size of the size x size square with largest total power.
    
    Parameters
    -------
    power - numpy array of fuel cell power level
    
    Returns
    -------
    Size of size x size square
    Top-left fuel cell coordinates of largest total power size x size square.
    Total power associated to square.
    """
	maxes = []
	max_ind = []
	for size in range(1,301):
		ind, mxx = largest_power(power, size)
		maxes.append(mxx)
		max_ind.append(ind)
	return np.argmax(maxes)+1, max_ind[np.argmax(maxes)], np.max(maxes)


# PART 1
# Tests

#power = power_fuel(57, [122,79])
#power = power_fuel(39, [217,196])
#power = power_fuel(71, [101,153])
#power = power_fuel(18, [33,45])

power = power_fuel(5468) #puzzle input
print largest_power(power, 3)

# PART 2
print largest_power_sizes(power)
	
