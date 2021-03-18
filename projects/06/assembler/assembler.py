#!/usr/bin/env python3

import argparse
from typing import List, Dict


class Assembler:
    def __init__(self, input_file: str, output_file: str):
        self.lines: List[str] = []
        self.symbols: Dict[str, int] = {}
        self.input_file: str = input_file
        self.output_file: str = output_file
        self.binary: List[str] = []
        self.variable_address: int = 16
        self.variables: Dict[str, int] = {}
        self.predefined_symbols: Dict[str, int] = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        self.jump_table: Dict[str, str] = {
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }
        self.instruction_table: Dict[str, str] = {
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101",
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
        }
    
    def run(self):
        self.first_pass()
        self.second_pass()
        with open(self.output_file, mode='wt', encoding='utf-8') as f:
            f.write('\n'.join(self.binary))

    def first_pass(self):
        '''
        Generate the symbols table with all the labels
        Also remove comments and empty spaces 
        '''
        with open(self.input_file) as f:
            line_counter: int = 0
            for line in f:
                line = line.strip()
                if not line or line[:2] == "//":
                    continue
                if line[0] == '(':
                    self.symbols[line[1:-1]] = line_counter
                    continue
                self.lines.append(line.split()[0])
                line_counter += 1
    
    def second_pass(self):
        '''
        Translate the text from asm to hack
        '''
        for line in self.lines:
            if line[0] == '@':
                self.binary.append(self.a_func(line))
            else:
                self.binary.append(self.c_func(line))

    def a_func(self, line: str) -> str:
        '''
        @ function translation
        '''
        line = line[1:]
        value = 0
        if line.isnumeric():
            value = int(line)
        elif line in self.predefined_symbols:
            value = self.predefined_symbols[line]
        elif line in self.symbols:
            value = self.symbols[line]
        elif line in self.variables:
            value = self.variables[line]
        else:
            self.variables[line] = self.variable_address
            value = self.variables[line]
            self.variable_address += 1
        return "{0:b}".format(value).zfill(16)

    def c_func(self, line: str) -> str:
        '''
        c function translation
        '''
        dest_bin = "000"
        if '=' in line:
            dest, line = line.split('=')
            for d in dest:
                if d == 'A':
                    dest_bin = '1' + dest_bin[1:]
                elif d == 'D':
                    dest_bin = dest_bin[0] + '1' + dest_bin[2]
                elif d == 'M':
                    dest_bin = dest_bin[:-1] + '1'

        jmp_bin = "000"
        if ';' in line:
            line, jmp = line.split(';')
            jmp_bin = self.jump_table[jmp]
        
        comp_bin = self.instruction_table[line]

        return "111" + comp_bin + dest_bin + jmp_bin


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Input file path")
    parser.add_argument("-o", "--output", type=str, help="Output file path")

    args = parser.parse_args()

    assembler = Assembler(args.input, args.output)
    assembler.run()