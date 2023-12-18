from aoc import run
from typing import List
from collections import namedtuple

CYCLE_LEN = 1000000000
ROCK = 'O'
SOLID = '#'
Position = namedtuple('Position', 'x, y')

def find_cycle(numbers, min_cycle_count=10):
    if len(numbers) <= min_cycle_count:
        return None

    slow_pointer = 1
    fast_pointer = 2

    while numbers[slow_pointer] != numbers[fast_pointer]:
        slow_pointer += 1
        fast_pointer += 2
        if fast_pointer >= len(numbers):
            return None

    cycle_start_index = 0
    slow_pointer = 0
    while numbers[slow_pointer] != numbers[fast_pointer]:
        slow_pointer += 1
        fast_pointer += 1
        cycle_start_index += 1
        if fast_pointer >= len(numbers):
            return None

    cycle_len = 1
    fast_pointer = slow_pointer + 1
    while numbers[slow_pointer] != numbers[fast_pointer]:
        fast_pointer += 1
        cycle_len += 1
        if fast_pointer >= len(numbers):
            return None

    return cycle_start_index, cycle_len

def parse_input(lines, value: str):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == value:
                yield Position(x, y), char

def get_rocks_load(rocks, max_pos):
    return sum(max_pos.x - x for x, _ in sorted(rocks))

def get_first(lines):
    max_pos = Position(len(lines), len(lines[0]))
    solids = {pos for pos, _ in parse_input(lines, SOLID)}
    rocks = [pos for pos, _ in parse_input(lines, ROCK)]

    moved_rocks = move(rocks, solids, max_pos, Position(-1, 0))
    return get_rocks_load(moved_rocks, max_pos)

def move(rocks, solids, max_pos, diff_pos):
    new_rocks: List[Position] = []
    new_solids = set()

    index = 0 if diff_pos.x != 0 else 1
    reverse = diff_pos.x > 0 or diff_pos.y > 0

    for rock in sorted(rocks, key=lambda x: x[index], reverse=reverse):
        new_rock = rock
        while True:
            new_x = new_rock.x + diff_pos.x
            new_y = new_rock.y + diff_pos.y
            new_position = Position(new_x, new_y)
            if new_x < 0 or new_x >= max_pos.x:
                break
            if new_y < 0 or new_y >= max_pos.y:
                break
            if new_position in solids or new_position in new_solids:
                break
            new_rock = new_position
        new_rocks.append(new_rock)
        new_solids.add(new_rock)
    return new_rocks

def get_second(lines):
    max_pos = Position(len(lines), len(lines[0]))
    solids = {pos for pos, _ in parse_input(lines, SOLID)}
    rocks = [pos for pos, _ in parse_input(lines, ROCK)]

    loads = []
    for _ in range(CYCLE_LEN):
        rocks = move(rocks, solids, max_pos, Position(-1, 0))
        rocks = move(rocks, solids, max_pos, Position(0, -1))
        rocks = move(rocks, solids, max_pos, Position(1, 0))
        rocks = move(rocks, solids, max_pos, Position(0, 1))

        loads.append(get_rocks_load(rocks, max_pos))
        cycle = find_cycle(loads)
        if not cycle:
            continue

        cycle_start, cycle_len = cycle
        index = cycle_start + (CYCLE_LEN - cycle_start) % cycle_len - 1
        return loads[index]

    return sum(loads)

if __name__ == '__main__':
    run(get_first, get_second)
