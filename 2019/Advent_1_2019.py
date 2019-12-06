# -*- coding: utf-8 -*-
import numpy as np


def find_fuel(mass):
    """mass - Number"""
    return np.floor(mass/3) - 2
    
def fuel_counter_upper(modules_mass_array):
    """For array of numbers int/float, return sum of fuels"""
    return find_fuel(modules_mass_array).sum()


INPUT_DATA = np.array(open("Advent_1_2019_input.txt", "r").read().splitlines()).astype(float)
    
#PART 1
FUEL_INPUT = fuel_counter_upper(INPUT_DATA)
print(FUEL_INPUT)



#PART 2
def additional_fuel(mass):
    count = -mass
    while mass > 0:
        count += mass
        mass = find_fuel(mass)
    return count
    
total_fuel = 0
for mass in INPUT_DATA:
    total_fuel += additional_fuel(mass)
print(total_fuel)