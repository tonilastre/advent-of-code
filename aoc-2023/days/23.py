from aoc import run
from queue import Queue
from functools import cache
from typing import Dict, Tuple, List, Iterator, Set
from collections import namedtuple

ROCK = '#'
EMPTY = '.'

Position = namedtuple('Position', 'x, y')

DIFF_BY_SLOPE: Dict[str, Position] = {
    '<': Position(0, -1),
    '>': Position(0, 1),
    'v': Position(1, 0),
    '^': Position(-1, 0),
}

def parse_line(line: str) -> Tuple[int, str]:
    for y, char in enumerate(line):
        yield y, char

def parse_lines(lines: List[str]) -> Iterator[Tuple[Position, str]]:
    for x, line in enumerate(lines):
        for y, char in parse_line(line):
            yield Position(x, y), char

def get_start_position(lines: List[str]) -> Position:
    return Position(
        0,
        next(y for y, char in parse_line(lines[0]) if char == EMPTY)
    )

def get_end_position(lines: List[str]) -> Position:
    return Position(
        len(lines) - 1,
        next(y for y, char in parse_line(lines[-1]) if char == EMPTY)
    )

def is_in_map(pos: Position, max_x: int, max_y: int):
    return 0 <= pos.x < max_x and 0 <= pos.y < max_y

def iter_adj_positions(pos: Position) -> Iterator[Position]:
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = pos.x + dx
        new_y = pos.y + dy
        yield Position(new_x, new_y)

def get_directional_path(
    positions: Set[Position],
    start_pos: Position,
    next_pos: Position
) -> List[Position]:
    path: List[Position] = [start_pos]
    visited: Set[Position] = set()
    visited.add(start_pos)
    current_pos = next_pos

    while True:
        path.append(current_pos)
        visited.add(current_pos)

        adj_positions = [
            adj_pos
            for adj_pos in iter_adj_positions(current_pos)
            if adj_pos not in visited and adj_pos in positions
        ]
        if len(adj_positions) != 1:
            break
        current_pos = adj_positions[0]
    return path

def get_crossing_distances(
    start_pos: Position,
    positions: Set[Position],
) -> Dict[Tuple[Position, Position], int]:
    queue = Queue()
    start_next_pos = next(p for p in iter_adj_positions(start_pos) if p in positions)
    queue.put((start_pos, start_next_pos))

    distances: Dict[Tuple[Position, Position], int] = dict()
    visited: Set[Position] = set()

    while not queue.empty():
        current_pos, next_pos = queue.get()
        path = get_directional_path(positions, current_pos, next_pos)
        distances[(path[0], path[-1])] = len(path) - 1
        visited.update(path)
        for adj_pos in iter_adj_positions(path[-1]):
            if adj_pos not in positions:
                continue
            if adj_pos in visited:
                continue
            queue.put((path[-1], adj_pos))
    return distances

@cache
def find_max_dist(index, end_index, edges, visited_bits):
    if index == end_index:
        return True, 0

    visited_bits = visited_bits | (2 ** index)

    max_dist = 0
    is_max_found = False
    for next_index, next_dist in edges[index]:
        if (2 ** next_index) & visited_bits != 0:
            continue

        is_found, dist = find_max_dist(
            next_index,
            end_index,
            edges,
            visited_bits
        )
        if not is_found:
            continue

        total_dist = dist + next_dist
        if total_dist > max_dist:
            max_dist = total_dist
            is_max_found = True

    return is_max_found, max_dist

def get_first(lines):
    max_x, max_y = len(lines), len(lines[0])
    map = {pos: char for pos, char in parse_lines(lines) if char != EMPTY}
    start_pos = get_start_position(lines)
    end_pos = get_end_position(lines)

    max_dist_by_pos: Dict[Position, int] = {
        start_pos: 0
    }
    queue = Queue()
    queue.put((0, None, start_pos))

    while not queue.empty():
        dist, prev_pos, pos = queue.get()
        if not is_in_map(pos, max_x, max_y):
            continue

        value = map.get(pos)
        if value == ROCK:
            continue

        max_dist = max_dist_by_pos.get(pos) or 0
        max_dist_by_pos[pos] = max(max_dist, dist)

        adj_positions: List[Position] = []
        if value in DIFF_BY_SLOPE:
            dx, dy = DIFF_BY_SLOPE[value]
            adj_positions.append(Position(pos.x + dx, pos.y + dy))
        elif not value:
            adj_positions = list(iter_adj_positions(pos))

        for adj_pos in adj_positions:
            if adj_pos != prev_pos:
                queue.put((dist + 1, pos, adj_pos))

    return max_dist_by_pos[end_pos]

def get_second(lines):
    positions = {pos for pos, char in parse_lines(lines) if char != ROCK}
    start_pos = get_start_position(lines)
    end_pos = get_end_position(lines)

    distances = get_crossing_distances(start_pos, positions)

    last_index = 0
    edges: List[List[Tuple[Position, int]]] = []
    index_by_pos: Dict[Position, int] = dict()

    for path, dist in distances.items():
        for position in path:
            if position not in index_by_pos:
                index_by_pos[position] = last_index
                edges.append([])
                last_index += 1

        start, end = path
        start_index = index_by_pos[start]
        end_index = index_by_pos[end]
        edges[start_index].append((end_index, dist))
        edges[end_index].append((start_index, dist))

    _, max_dist = find_max_dist(
        index_by_pos[start_pos],
        index_by_pos[end_pos],
        tuple(tuple(e) for e in edges),
        0,
    )
    return max_dist

if __name__ == '__main__':
    run(get_first, get_second)
