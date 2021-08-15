import re
import argparse

SIZE = 30000

def init_parser():
    parser = argparse.ArgumentParser('brainfuck interpreter!')
    parser.add_argument('brainfuck_file', metavar='file', type=str,
                        help='Name of brainfuck program.')
    return parser


def match_brackets(brain):
    left = []
    match = {}

    i = 0
    for cmd in brain:
        if cmd == '[':
            left.append(i)
        elif cmd == ']':
            if len(left) == 0:
                raise SyntaxError(f"Couldn't find matching closing bracket for {i}")
            j = left.pop()
            match[j] = i
            match[i] = j
        i += 1

    if len(left) > 0:
        raise SyntaxError(f"Couldn't find matching closing bracket for {i}")
    print(f"bracket positions: {match}")
    return match

def fuck(brain):
    match = match_brackets(brain)

    data = [0 for i in range(SIZE)]
    data_pointer = 0
    instruction_pointer = 0

    for cmd in brain:
        print(data[:data_pointer])
        if cmd == '+':
            data[data_pointer] += 1
        elif cmd == '-':
            data[data_pointer] -= 1
        elif cmd == '>':
            if data_pointer < SIZE:
                data_pointer += 1
            else:
                raise IndexError("Data pointer reached out of range")
        elif cmd == '<':
            if data_pointer > 0:
                data_pointer -= 1
            else:
                raise IndexError("Data pointer reached out of range")           
        elif cmd == '.':
            print(chr(data[data_pointer]), end='')
        elif cmd == ',':
            while 1:
                j = int(input("> "))
                if 0 <= data <= 127:
                    break
                raise ValueError("Input must be an integer less than 127!")
            data[data_pointer] = j
        elif cmd == '[':
            if data[data_pointer] == 0:
                instruction_pointer = match[instruction_pointer]
        elif cmd == ']':
            if data[data_pointer] != 0:
                instruction_pointer = match[instruction_pointer]
        instruction_pointer += 1
        

def get_fucked(brain):
    with open(brain, 'r') as f:
        program = f.read()
        # filter comments out
        program = re.sub('[^\+\-<>.,\[\]]', '', program) 
        print(f"Input: {program}")

        return program

if __name__ == "__main__":
    args = init_parser().parse_args()
    brain = get_fucked(args.brainfuck_file)
    fuck(brain)
