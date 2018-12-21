from copy import deepcopy
import logging

#Setting logging preferences
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Register():
    """"""
    def __init__(self, r, instruction=[]):
        self.reg = deepcopy(r)
        self.opcodes = {'addi': self.addi, 
                        'addr': self.addr, 
                        'bani': self.bani, 
                        'banr': self.banr,
                        'bori': self.bori, 
                        'borr': self.borr,
                        'eqir': self.eqir,
                        'eqri': self.eqri,
                        'eqrr': self.eqrr,
                        'gtir': self.gtir,
                        'gtri': self.gtri,
                        'gtrr': self.gtrr,
                        'muli': self.muli,
                        'mulr': self.mulr,
                        'seti': self.seti,
                        'setr':self.setr,
                        }
        self.num_op_dict = {}
        self.instruction = []
        if instruction:
            self.get_instruction(instruction)
    
    
    def get_instruction(self, instruction):
        assert len(instruction) == 4, "Invalid instruction, length must be 4."
        self.instruction = instruction[1:]
        if str(instruction[0]).isdigit():
            self.op_num = int(instruction[0])
            self.op = ""
        elif instruction[0] in self.opcodes.keys():
            self.op_num = ""
            self.op = instruction[0]
        else:
            logger.error("Invalid first argument of instruction: {}".format(instruction[0]))
    
    def addr(self, a, b, c): 
        self.reg[c] = self.reg[a] + self.reg[b]
    
    def addi(self, a, b, c):
        self.reg[c] = self.reg[a] + b
    
    def mulr(self, a, b, c):
        self.reg[c] = self.reg[a] * self.reg[b]
    
    def muli(self, a, b, c):
        self.reg[c] = self.reg[a] * b
    
    def banr(self, a, b, c):
        self.reg[c] = self.reg[a] & self.reg[b]
    
    def bani(self, a, b, c):
        self.reg[c] = self.reg[a] & b
    
    def borr(self, a, b, c):
        self.reg[c] = self.reg[a] | self.reg[b]
    
    def bori(self, a, b, c):
        self.reg[c] = self.reg[a] | b
    
    def setr(self, a, b, c):
        self.reg[c] = self.reg[a]
    
    def seti(self, a, b, c):
        self.reg[c] = a
    
    def gtir(self, a, b, c):
        if a > self.reg[b]:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    def gtri(self, a, b, c):
        if self.reg[a] > b:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    def gtrr(self, a, b, c):
        if self.reg[a] > self.reg[b]:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    def eqir(self, a, b, c):
        if a == self.reg[b]:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    def eqri(self, a, b, c):
        if self.reg[a] == b:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    def eqrr(self, a, b, c):
        if self.reg[a] == self.reg[b]:
            self.reg[c] = 1
        else:
            self.reg[c] = 0
    
    
    def do_instruction(self, op="", instruction=[]):
        if instruction:
            self.get_instruction(instruction)
        if not instruction and not self.instruction:
            logger.error("Need at least an instruction")
        
        if op and op in self.opcodes.keys():
            self.opcodes[op](*self.instruction)
        elif type(self.op_num) == int:
            self.opcodes[self.num_op_dict[self.op_num]](*self.instruction)
        elif self.op:
            self.opcodes[self.op](*self.instruction)
        else:
            logger.error("Need at least an opcode or opcode number!")
    
    
    def do_instructions(self, instructions):
        if len(self.num_op_dict.keys()) == 0:
            logger.error("Need samples to learn number-opcode equivalence, and run learn_opcode_numbers")
        for instr in instructions:
            self.do_instruction(instruction=instr)
        return self.reg
    
    
    def learn_opcode_numbers(self, samples):
        """
        List of samples : [register before, instruction, register after]
        """
        op_num_possibilities = {op:[] for op in self.opcodes.keys()} #{op:op_num possibilities}
        for reg in samples:
            for opcd in self.opcodes.keys():
                obj = Register(reg[0], instruction=reg[1])
                new_reg = obj.do_instruction(op=opcd)
                if new_reg == reg[2]:
                    if reg[1][0] not in op_num_possibilities[opcd]:
                        op_num_possibilities[opcd].append(reg[1][0])
        
        while True:
            for op in op_num_possibilities.keys():
                if len(op_num_possibilities[op]) == 1:
                    index = op_num_possibilities[op][0]
                    self.num_op_dict[index] = op
                    del op_num_possibilities[op]
                    for vals in op_num_possibilities.values():
                        if index in vals:
                            vals.remove(index)
            if len(self.num_op_dict) == len(self.opcodes.keys()):
                break
    
    def do_ip_instructions(self, instructions, ip):
        self.ip = ip
        counter_ip = self.reg[self.ip]
        while counter_ip < len(instructions):
            self.reg[self.ip] = counter_ip
            self.do_instruction(instruction=instructions[counter_ip])
            counter_ip = self.reg[self.ip] + 1



def parse_samples(fname):
    registers = [[]]
    with open(fname, "r") as f:
        for line in f:
            line = line.rstrip("]\n")
            if line.startswith("Before") or line.startswith("After"):
                line = line.split("[")
                registers[-1].append([int(i) for i in line[1].split(", ")])
            elif line == "":
                registers.append([])
            else:
                registers[-1].append([int(i) for i in line.split(" ")])
    return registers

def parse_test_program(fname):
    instructions = []
    ip = ""
    with open(fname, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#ip"):
                ip = int(line.split()[1])
            else:
                try:
                    instructions.append([int(i) for i in line.split(" ")])
                except:
                    instructions.append([line.split()[0]]+[int(i) for i in line.split(" ")[1:]])
    return ip, instructions


samples = parse_samples("Advent_16_input_part1.txt")
opcodes = ['addi', 'addr', 'bani', 'banr', 'bori', 'borr', 'eqir', 'eqri', 'eqrr', 'gtir', 'gtri', 'gtrr', 'muli', 'mulr', 'seti', 'setr']
op_reg = []
for reg in samples:
    op_reg.append([])
    for opcd in opcodes:
        obj = Register(reg[0], instruction=reg[1])
        new_reg = obj.do_instruction(op=opcd)
        if new_reg == reg[2]:
            op_reg[-1].append(opcd)

counts = 0
for re in op_reg:
    if len(re) >= 3:
        counts += 1

print counts

#Part 2

_, instructions = parse_test_program("Advent_16_input_part2.txt")
test = Register([0,0,0,0])
test.learn_opcode_numbers(samples)
test.do_instructions(instructions)
print test.reg[0]


#Advent 19
ip, program = parse_test_program("Advent_19_input.txt")
prog = Register([0,0,0,0,0])
prog.do_ip_instructions(program, ip)
