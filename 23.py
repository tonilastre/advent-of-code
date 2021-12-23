import re
from aoc import run
from queue import SimpleQueue
from copy import copy
from functools import lru_cache

COST_BY_LETTER = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }
COLUMN_BY_LETTER = { 'A': 2, 'B': 4, 'C': 6, 'D': 8 }

HALLWAY_SIZE = 11
ROOM_SIZE = 4

def print_positions(positions):
    max_rows = max(p[0] for p in positions) + 1
    max_cols = max(p[1] for p in positions) + 1

    for i in range(max_rows):
        line = ((positions[(i, j)] or '.') if (i, j) in positions else ' ' for j in range(max_cols))
        print(''.join(line))

def get_input_as_positions(lines):
    letter_lines = []
    for line in lines:
        letters = re.findall('[A-Z]', line)
        if letters:
            letter_lines.append(letters)

    positions = {}
    for i in range(HALLWAY_SIZE):
        positions[(0, i)] = ''

    for i, letters in enumerate(letter_lines):
        for j, letter in enumerate(letters):
            positions[(i + 1, (j + 1) * 2)] = letter

    return positions

def iter_adj_positions(position):
    i, j = position
    yield from ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))

def iter_reachable_moves(current_position, positions):
    queue = SimpleQueue()
    queue.put(current_position)
    visited_positions = set(current_position)

    while not queue.empty():
        next_position = queue.get()
        visited_positions.add(next_position)

        for adj_position in iter_adj_positions(next_position):
            if adj_position not in positions:
                continue
            if adj_position in visited_positions:
                continue
            if positions[adj_position] == '':
                queue.put(adj_position)
                yield (current_position, adj_position)

def get_possible_room_position(letter, positions):
    column = COLUMN_BY_LETTER[letter]

    for row in range(ROOM_SIZE, 0, -1):
        position = (row, column)
        if position not in positions:
            continue
        if positions[position] == '':
            return position
        if positions[position] != letter:
            break

    return None

def is_final_room_position(current_position, positions):
    letter = positions[current_position]
    column = COLUMN_BY_LETTER[letter]

    if column != current_position[1]:
        return False

    for row in range(current_position[0] + 1, ROOM_SIZE + 1):
        position = (row, column)
        if position in positions and positions[position] != letter:
            return False
    return True

def is_hallway_position(position):
    return position[0] == 0

def is_room_position(position):
    return position[0] > 0

def filter_possible_moves(moves, positions):
    invalid_positions = { (0, v) for v in COLUMN_BY_LETTER.values() }

    for move in moves:
        current_position, next_position = move
        letter = positions[current_position]

        # Invalid positions (top of the room)
        if next_position in invalid_positions:
            continue

        if is_hallway_position(current_position):
            room_position = get_possible_room_position(letter, positions)
            if next_position == room_position:
                yield move
            continue

        if is_room_position(current_position):
            if not is_final_room_position(current_position, positions) and is_hallway_position(next_position):
                yield move
            continue

def iter_possible_moves(positions):
    for current_position, letter in positions.items():
        if not letter:
            continue
        moves = iter_reachable_moves(current_position, positions)
        yield from filter_possible_moves(moves, positions)

def is_solved(positions):
    for letter, column in COLUMN_BY_LETTER.items():
        for row in range(1, ROOM_SIZE + 1):
            if (row, column) in positions and positions[(row, column)] != letter:
                return False
    return True

def get_move_cost(move, positions):
    from_position, to_position = move
    letter = positions[to_position]

    distance = abs(to_position[1] - from_position[1]) + abs(to_position[0] - from_position[0])
    return distance * COST_BY_LETTER[letter]

def to_tuple(positions):
    return tuple((position, value) for position, value in positions.items())

def from_tuple(positions):
    return { position: value for position, value in positions }

@lru_cache(maxsize=None)
def solve(positions):
    positions = from_tuple(positions)
    if is_solved(positions):
        return True, 0

    possible_moves = list(iter_possible_moves(positions))
    if not possible_moves:
        return False, 0

    solved_min_cost = None

    for possible_move in possible_moves:
        from_position, to_position = possible_move

        new_positions = copy(positions)
        new_positions[to_position] = new_positions[from_position]
        new_positions[from_position] = ''

        move_cost = get_move_cost(possible_move, new_positions)
        is_sub_solved, sub_cost = solve(to_tuple(new_positions))

        if not is_sub_solved:
            continue

        current_cost = move_cost + sub_cost
        if solved_min_cost is None or current_cost < solved_min_cost:
            solved_min_cost = current_cost

    return solved_min_cost is not None, solved_min_cost

def get_first(lines):
    positions = get_input_as_positions(lines)
    _, cost = solve(to_tuple(positions))
    return cost

def get_second(lines):
    new_lines = lines[:-2] + ['  #D#C#B#A#', '  #D#B#A#C#'] + lines[-2:]
    positions = get_input_as_positions(new_lines)
    _, cost = solve(to_tuple(positions))
    return cost

if __name__ == '__main__':
    run(get_first, get_second)
