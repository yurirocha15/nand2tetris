from typing import List

class Writer:
    def __init__(self, dest_file: str):
        self.dest_file: str = dest_file
        self.commands: List[str] = []

    def add_command(self, cmds: List[str]):
        self.commands.extend(cmds)
    
    def write(self):
        with open(self.dest_file, 'w') as file:
            file.writelines(map(lambda line: line + "\n", self.commands))
    
    def set_dest_file(self, dest_file: str):
        self.dest_file = dest_file