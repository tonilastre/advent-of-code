from aoc import run
from queue import Queue
from typing import Set, Tuple, List
from collections import namedtuple

Position = namedtuple('Position', 'x, y')

def get_diffs_by_value(value: str, diff: Position):
    dx, dy = diff
    if value == '-':
        return [Position(dx, dy)] if dy else [Position(0, -1), Position(0, 1)]
    if value == '|':
        return [Position(dx, dy)] if dx else [Position(-1, 0), Position(1, 0)]
    if value == '\\':
        return [Position(0, dx)] if dx else [Position(dy, 0)]
    if value == '/':
        return [Position(0, -dx)] if dx else [Position(-dy, 0)]

def parse_input(lines):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char != '.':
                yield Position(x, y), char

def is_in_map(pos: Position, max_x: int, max_y: int):
    return 0 <= pos.x < max_x and 0 <= pos.y < max_y

def get_visited_count(map, max_x, max_y, start_position, start_diff):
    queue = Queue()
    queue.put((start_position, start_diff))
    visited_positions: Set[Position] = set()
    visited_values: Set[Tuple[Position, Position]] = set()

    while not queue.empty():
        pos, diff = queue.get()
        if not is_in_map(pos, max_x, max_y):
            continue

        visited_positions.add(pos)
        if pos not in map:
            queue.put((Position(pos.x + diff.x, pos.y + diff.y), diff))
            continue

        value = map[pos]
        if (pos, diff) in visited_values:
            continue

        visited_values.add((pos, diff))
        new_diffs = get_diffs_by_value(value, diff)
        for new_diff in new_diffs:
            queue.put((Position(pos.x + new_diff.x, pos.y + new_diff.y), new_diff))

    return len(visited_positions)

def get_first(lines):
    max_x, max_y = len(lines), len(lines[0])
    map = {pos: char for pos, char in parse_input(lines)}
    return get_visited_count(
        map,
        max_x=max_x,
        max_y=max_y,
        start_position=Position(0, 0),
        start_diff=Position(0, 1),
    )

def get_second(lines):
    max_x, max_y = len(lines), len(lines[0])
    map = {pos: char for pos, char in parse_input(lines)}

    moves: List[Tuple[Position, Position]] = []
    for x in range(max_x):
        moves.append((Position(x, 0), Position(0, 1)))
        moves.append((Position(x, max_y - 1), Position(0, -1)))
    for y in range(max_y):
        moves.append((Position(0, y), Position(1, 0)))
        moves.append((Position(max_x - 1, y), Position(-1, 0)))

    max_count = 0
    for start_position, start_diff in moves:
        count = get_visited_count(
            map,
            max_x=max_x,
            max_y=max_y,
            start_position=start_position,
            start_diff=start_diff,
        )
        max_count = max(max_count, count)
    return max_count

if __name__ == '__main__':
    run(get_first, get_second)
