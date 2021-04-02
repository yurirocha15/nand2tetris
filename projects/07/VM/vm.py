#!/usr/bin/env python3

import argparse
from vm_parser import Parser
from vm_writter import Writer

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Input file path")
    parser.add_argument("-o", "--output", type=str, help="Output file path")

    args = parser.parse_args()

    parser = Parser(args.input)
    writer = Writer(args.output)

    while parser.has_more_commands():
        writer.add_command(parser.parse_next())
    
    writer.write()