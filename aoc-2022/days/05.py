import re
from collections import namedtuple
from aoc import run, get_int_numbers

Move = namedtuple('Move', 'count, from_index, to_index')

def iter_match_index_values(regex, *lines):
    for line in lines:
        for value_match in re.finditer(regex, line):
            value = value_match.group()
            index = value_match.start()
            yield index, value

def parse_input_state(lines):
    reversed_lines = reversed(lines)
    number_by_index = {}

    for index, number in iter_match_index_values(r'(\d)', next(reversed_lines)):
        number_by_index[index] = int(number)

    max_number = max(number_by_index.values())
    states = [[] for _ in range(max_number + 1)]

    for index, letter in iter_match_index_values(r'([A-Z])', *reversed_lines):
        states[number_by_index[index]].append(letter)

    return states

def parse_input_moves(lines):
    for line in lines:
        yield Move(*get_int_numbers(line))

def parse_input(lines):
    empty_line_index = next(i for i, line in enumerate(lines) if not line.strip())
    state_lines = lines[:empty_line_index]
    moves_lines = lines[empty_line_index + 1:]

    return parse_input_state(state_lines), parse_input_moves(moves_lines)

def get_first(lines):
    states, moves = parse_input(lines)
    for move in moves:
        for _ in range(move.count):
            states[move.to_index].append(states[move.from_index].pop())

    return ''.join(state[-1] for state in states if state)

def get_second(lines):
    states, moves = parse_input(lines)
    for move in moves:
        temp_stack = [states[move.from_index].pop() for _ in range(move.count)]
        states[move.to_index].extend(reversed(temp_stack))

    return ''.join(state[-1] for state in states if state)

if __name__ == '__main__':
    run(get_first, get_second)
