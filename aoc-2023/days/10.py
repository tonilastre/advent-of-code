from aoc import run
from typing import Dict, Set, List, Tuple
from collections import namedtuple, defaultdict

Position = namedtuple('Position', 'x, y')

DIFFS_BY_CHAR = {
    '-': [(0, -1), (0, 1)],
    '7': [(0, -1), (1, 0)],
    '|': [(-1, 0), (1, 0)],
    'L': [(-1, 0), (0, 1)],
    'J': [(-1, 0), (0, -1)],
    'F': [(1, 0), (0, 1)],
}

def parse_lines(lines):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            yield Position(x, y), char

def iter_edge_positions(position, char):
    for dx, dy in DIFFS_BY_CHAR[char]:
        yield Position(position.x + dx, position.y + dy)

def iter_adj_positions(position):
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = position.x + dx
        new_y = position.y + dy
        yield Position(new_x, new_y)

def get_start_position_value(map):
    start_position = next((position for position, value in map.items() if value == 'S'))
    start_diffs: List[Tuple[int, int]] = []

    for adj_position in iter_adj_positions(start_position):
        if adj_position not in map:
            continue
        edge_positions = iter_edge_positions(adj_position, map[adj_position])
        if all(start_position != edge_position for edge_position in edge_positions):
            continue
        start_diffs.append((adj_position.x - start_position.x, adj_position.y - start_position.y))

    for char, diffs in DIFFS_BY_CHAR.items():
        if sorted(diffs) == sorted(start_diffs):
            return start_position, char

def enumerate_path_positions(map: Dict[Position, str], start_position: Position):
    visited_positions: Set[Position] = set()
    positions: List[Position] = [start_position]
    step = 0

    while positions:
        new_positions: List[Position] = []
        for position in positions:
            yield (step, position)
            visited_positions.add(position)
            for edge_position in iter_edge_positions(position, map[position]):
                if edge_position not in map:
                    continue
                if edge_position in visited_positions:
                    continue
                new_positions.append(edge_position)
        step += 1
        positions = new_positions

def get_first(lines):
    map = {position: char for position, char in parse_lines(lines) if char != '.'}
    start_position, char = get_start_position_value(map)
    map[start_position] = char
    return max(step for step, _ in enumerate_path_positions(map, start_position))

def get_second(lines):
    map = {position: char for position, char in parse_lines(lines) if char != '.'}
    start_position, char = get_start_position_value(map)
    map[start_position] = char
    path_positions = set(
        position
        for _, position
        in enumerate_path_positions(map, start_position)
    )

    cross_positions_by_x: Dict[int, List[Position]] = defaultdict(list)
    for path_position in path_positions:
        if map[path_position] != '-':
            cross_positions_by_x[path_position.x].append(path_position)
    for key in cross_positions_by_x.keys():
        cross_positions_by_x[key] = sorted(cross_positions_by_x[key])

    inside_positions: List[Position] = []

    for position, _ in parse_lines(lines):
        if position in path_positions:
            continue

        cross_positions = [
            p
            for p in cross_positions_by_x[position.x]
            if p.y > position.y
        ]
        if not cross_positions:
            continue

        cross_count = 0
        prev_cross_value: str = ''
        for cross_position in cross_positions:
            cross_value = map[cross_position]
            cross_values = f'{prev_cross_value}{cross_value}'

            if cross_values in ['FJ', 'L7'] or cross_value == '-':
                prev_cross_value = cross_value
                continue

            prev_cross_value = cross_value
            cross_count += 1

        if cross_count % 2 == 1:
            inside_positions.append(position)

    return len(inside_positions)

if __name__ == '__main__':
    run(get_first, get_second)
