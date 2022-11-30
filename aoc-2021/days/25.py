from aoc import run
from itertools import chain

LEFT_CHAR = '>'
BOTTOM_CHAR = 'v'

def parse_input(lines):
    size = (len(lines), len(lines[0]))
    positions = dict()
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == 'v' or char == '>':
                positions[(row, column)] = char
    return positions, size

def get_next_move(current_position, positions, size):
    rows, cols = size
    char = positions[current_position]

    if char == LEFT_CHAR:
        new_position = (current_position[0], (current_position[1] + 1) % cols)
    if char == BOTTOM_CHAR:
        new_position = ((current_position[0] + 1) % rows, current_position[1])

    return (current_position, new_position) if new_position else None

def iter_possible_next_moves(positions, size, filter_char):
    for position, char in positions.items():
        if char != filter_char:
            continue
        next_move = get_next_move(position, positions, size)
        if next_move and next_move[1] not in positions:
            yield next_move

def move(positions, size, step = 1):
    left_moves = list(iter_possible_next_moves(positions, size, filter_char = LEFT_CHAR))
    for current_position, new_position in left_moves:
        positions[new_position] = positions[current_position]
        del positions[current_position]

    bottom_moves = list(iter_possible_next_moves(positions, size, filter_char = BOTTOM_CHAR))
    for current_position, new_position in bottom_moves:
        positions[new_position] = positions[current_position]
        del positions[current_position]

    if len(left_moves) == 0 and len(bottom_moves) == 0:
        return step

    return move(positions, size, step + 1)

def get_first(lines):
    positions, size = parse_input(lines)
    return move(positions, size)

if __name__ == '__main__':
    run(get_first)
