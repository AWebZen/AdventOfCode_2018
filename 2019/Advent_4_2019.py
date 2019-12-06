# -*- coding: utf-8 -*-
from itertools import groupby

INPUT_DATA = [278384, 824795]

#==============================================================================
# PART 1
#==============================================================================
def find_password(input_data, lambda_cond):
    passwords = []
    for no in range(*input_data):
        no_list = list(str(no))
        repeats = [k for k, g in groupby(no_list) if lambda_cond(g)]
        if sorted(no_list) == no_list and len(repeats) != 0:
            passwords.append(no)
    return passwords

passwords = find_password(INPUT_DATA, lambda x: sum(1 for i in x) > 1)
print(len(passwords))

#==============================================================================
# PART 2
#==============================================================================
    
passwords2 = find_password(INPUT_DATA, lambda x: sum(1 for i in x) == 2)
print(len(passwords2))