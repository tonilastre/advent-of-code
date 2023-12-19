from heapq import heappush, heappop
from aoc import run
from typing import List, Set, Tuple
from collections import namedtuple

Position = namedtuple('Position', 'x, y')

def parse_input(lines):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            yield Position(x, y), int(char)

def is_in_map(pos: Position, max_x: int, max_y: int):
    return 0 <= pos.x < max_x and 0 <= pos.y < max_y

def get_shortest_host(map, min_dir_limit=0, max_dir_limit=3):
    max_x = max(pos.x for pos in map.keys()) + 1
    max_y = max(pos.y for pos in map.keys()) + 1

    start_position = Position(0, 0)
    end_position = Position(max_x - 1, max_y - 1)
    states: List[Tuple(Position, Position, int)] = []
    visited_states: Set[Tuple(int, Position, Position, int)] = set()

    heappush(states, (0, start_position, Position(0, 1), 0))
    heappush(states, (0, start_position, Position(1, 0), 0))

    while states:
        cost, position, move, count = heappop(states)
        if position == end_position:
            return cost

        new_moves: List[Tuple[Position, int]] = []
        if count < max_dir_limit:
            new_moves.append((move, count + 1))
        if count > min_dir_limit:
            new_moves.append((Position(-move.y, move.x), 1))
            new_moves.append((Position(move.y, -move.x), 1))

        for new_move, new_count in new_moves:
            new_position = Position(position.x + new_move.x, position.y + new_move.y)
            if not is_in_map(new_position, max_x, max_y):
                continue

            state = (new_position, new_move, new_count)
            if state in visited_states:
                continue

            new_cost = cost + map[new_position]
            heappush(states, (new_cost, new_position, new_move, new_count))
            visited_states.add(state)
    return -1

def get_first(lines):
    map = {pos: value for pos, value in parse_input(lines)}
    return get_shortest_host(map, min_dir_limit=0, max_dir_limit=3)

def get_second(lines):
    map = {pos: value for pos, value in parse_input(lines)}
    return get_shortest_host(map, min_dir_limit=3, max_dir_limit=10)

if __name__ == '__main__':
    run(get_first, get_second)
