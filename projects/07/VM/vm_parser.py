
import os
from typing import List, Dict, Set

class Parser:
    def __init__(self, input_file: str):
        self.file_name = os.path.basename(input_file)
        self.commands: List[List[str]] = []
        with open(input_file, "r") as file:
            for line in file:
                line = line.split('//')[0].strip()
                if line and line[0] != '/':
                    self.commands.append(line.split())
        
        self.current_command = 0
        self.comp_cnt = 0
        self._init_tables()

    def parse_next(self) -> List[str]:
        commands: List[str] = []
        if self.commands[self.current_command][0] == 'push':
            commands = self._push_cmd(self.commands[self.current_command][1], self.commands[self.current_command][2])
        elif self.commands[self.current_command][0] == 'pop':
            commands = self._pop_cmd(self.commands[self.current_command][1], self.commands[self.current_command][2])
        elif self.commands[self.current_command][0] in (self.operations.keys() | self.unary_operations.keys() | self.comp_operations.keys()):
            commands = self._arithmetic_cmd(self.commands[self.current_command][0])
        self.current_command += 1
        return commands

    def has_more_commands(self) -> bool:
        return self.current_command != len(self.commands)
    
    def _init_tables(self):
        self.block_segments: Dict[str, str] = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

        self.operations: Dict[str, str] = {
            "add": "D+A",
            "sub": "D-A",
            "and": "D&A",
            "or": "D|A",
        }

        self.unary_operations: Dict[str, str] = {
            "neg": "-D",
            "not": "!D",
        }

        self.comp_operations: Dict[str, str] = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }

    def _push_cmd(self, segment: str, value: str) -> List[str]:
        commands: List[str] = []
        commands.extend(self._load_memory_into_D(self._get_source(segment, value), segment=="constant"))
        if segment in self.block_segments:
            commands.extend(self._forward_D_to_index(value))
        commands.extend(self._push_D())
        return commands
    
    def _pop_cmd(self, segment: str, value: str) -> List[str]:
        commands: List[str] = []
        dest: str = self._get_source(segment, value)
        if segment in self.block_segments:
            commands.extend(self._load_memory_into_D(dest))
            commands.extend(self._forward_D_to_index(value, save_address=True))
            commands.extend(self._save_D_to_temp_reg())
        commands.extend(self._pop_into_D())
        commands.extend(self._store_D_into_memory(segment, dest))
        return commands
    
    def _arithmetic_cmd(self, cmd: str) -> List[str]:
        commands: List[str] = []
        commands.extend(self._pop_into_D())
        if cmd not in self.unary_operations:
            commands.extend(self._save_D_to_temp_reg())
            commands.extend(self._pop_into_D())
            commands.extend(self._load_temp_reg_to_A())
        commands.extend(self._handle_arithmetic(cmd))
        commands.extend(self._push_D())
        return commands

    def _handle_arithmetic(self, cmd: str) -> List[str]:
        if cmd in self.operations:
            return self._handle_operation(cmd)
        if cmd in self.unary_operations:
            return self._handle_unary_operation(cmd)
        return self._handle_logical_operation(cmd)

    def _handle_operation(self, cmd: str) -> List[str]:
        return ["D=" + self.operations[cmd]]
    
    def _handle_unary_operation(self, cmd: str) -> List[str]:
        return ["D=" + self.unary_operations[cmd]]

    def _handle_logical_operation(self, cmd: str) -> List[str]:
        self.comp_cnt += 1
        return ["D=D-A",
                "@comp_op.true." + str(self.comp_cnt),
                "D;" + self.comp_operations[cmd],
                "D=0",
                "@comp_op.end." + str(self.comp_cnt),
                "0;JMP",
                "(comp_op.true." + str(self.comp_cnt) + ")",
                "D=-1",
                "(comp_op.end." + str(self.comp_cnt) + ")"]

    def _pop_into_D(self) -> List[str]:
        return ["@SP",  # M = SP
                "AM=M-1",  # SP--
                "D=M"]  # D = *SP
    
    def _push_D(self) -> List[str]:
        return ["@SP",  # M = SP
                "A=M",  # M = *SP
                "M=D",  # *SP = D
                "@SP",  # M = SP
                "M=M+1"]  # SP--
    
    def _load_memory_into_D(self, source : str, is_constant: bool = False) -> List[str]:
        return ["@" + source,  # A = <memory_segment>/constant
                "D=A" if is_constant else "D=M"]  # D = constant / D = *<memory_segment>

    def _forward_D_to_index(self, idx: str, save_address: bool = False) -> List[str]:
        return ["@" + idx,  # A = index
                "A=D+A",  # A = <memory_segment> + index
                "D=A" if save_address else "D=M"]  # D = <memory_segment>[index] / <memory_segment> + index
    
    def _store_D_into_memory(self, segment: str, destination: str) -> List[str]:
        if segment in self.block_segments:
            return [*self._load_temp_reg_to_A(),
                    "M=D"]
        return ["@" + destination,
                "M=D"]
    
    def _save_D_to_temp_reg(self) -> List[str]:
        return ["@R13",
                "M=D"]
    
    def _load_temp_reg_to_A(self) -> List[str]:
        return ["@R13",
                "A=M"]

    def _get_source(self, segment: str, value: str) -> str:
        if segment in self.block_segments:
            return self.block_segments[segment]
        if segment == "constant":
            return str(value)
        if segment == "static":
            return self.file_name + "." + str(value)
        if segment == "temp":
            return str(int(value) + 5)
        if segment == "pointer":
            return value