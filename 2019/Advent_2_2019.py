# -*- coding: utf-8 -*-
import numpy as np
from copy import deepcopy

INPUT_DATA = np.array(open("Advent_2_2019_input.txt", "r").read().split(",")).astype(int)

#==============================================================================
# PART 1
#==============================================================================

#Step 1: restore the gravity assist program.
part1_input = deepcopy(INPUT_DATA)
part1_input[1] = 12
part1_input[2] = 2


#Step 2, run Intcode program
def run_intcode(intcode_program):
    for i in np.arange(0, len(intcode_program), 4):
        opcode = intcode_program[i:i+4]
        if opcode[0] == 99:
            break
        if opcode[0] == 1:
            intcode_program[opcode[3]] = intcode_program[opcode[1]] + intcode_program[opcode[2]]
        if opcode[0] == 2:
            intcode_program[opcode[3]] = intcode_program[opcode[1]] * intcode_program[opcode[2]]        
    return intcode_program[0]
    
print(run_intcode(part1_input))
    
#==============================================================================
# PART 2    
#==============================================================================

def get_n_v(input_data):
    for noun in np.arange(99):
        for verb in np.arange(99):
            part2_input = deepcopy(input_data)
            part2_input[1] = noun
            part2_input[2] = verb
            if run_intcode(part2_input) == 19690720:
                return noun, verb
                
n, v = get_n_v(INPUT_DATA)

print (100*n+v)