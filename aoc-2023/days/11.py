from aoc import run
from typing import List
from collections import namedtuple
from itertools import combinations

Position = namedtuple('Position', 'x, y')

def get_distance(p1: Position, p2: Position):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def parse_lines(lines):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char == '#':
                yield Position(x, y)

def iter_new_positions(
    positions: List[Position],
    max_x: int,
    max_y: int,
    expansion_size=2,
):
    x_expands = set(range(max_x))
    y_expands = set(range(max_y))
    for position in positions:
        x_expands.discard(position.x)
        y_expands.discard(position.y)

    for position in positions:
        dx = len([x for x in x_expands if x < position.x])
        dy = len([y for y in y_expands if y < position.y])
        yield Position(
            position.x + dx * (expansion_size - 1),
            position.y + dy * (expansion_size - 1),
        )

def get_first(lines):
    max_x, max_y = len(lines), len(lines[0])
    positions = sorted(parse_lines(lines))

    new_positions = iter_new_positions(positions, max_x, max_y)
    return sum(
        get_distance(p1, p2)
        for p1, p2
        in combinations(new_positions, 2)
    )

def get_second(lines):
    max_x, max_y = len(lines), len(lines[0])
    positions = sorted(parse_lines(lines))

    new_positions = iter_new_positions(positions, max_x, max_y, expansion_size=1_000_000)
    return sum(
        get_distance(p1, p2)
        for p1, p2
        in combinations(new_positions, 2)
    )

if __name__ == '__main__':
    run(get_first, get_second)
