from aoc import run
from typing import Set
from collections import namedtuple
from queue import PriorityQueue

Position = namedtuple('Position', 'x, y')

def enumerate_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            yield Position(i, j), matrix[i][j]

def iter_ajd_positions(matrix, position):
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = position.x + dx
        new_y = position.y + dy

        if 0 <= new_x < len(matrix) and 0 <= new_y < len(matrix[position.x]):
            yield Position(new_x, new_y)

def iter_positions_by_value(map, value):
    for map_position, map_value in enumerate_matrix(map):
        if map_value == value:
            yield map_position

def get_min_distance(map, start_position: Position, end_positions: Set[Position], is_accepted_move):
    queue = PriorityQueue()
    queue.put((0, start_position))
    visited_positions = {start_position}

    while not queue.empty():
        distance, position = queue.get()
        if position in end_positions:
            return distance

        current_value = map[position.x][position.y]
        for adj_position in iter_ajd_positions(map, position):
            if adj_position in visited_positions:
                continue

            adj_value = map[adj_position.x][adj_position.y]
            if is_accepted_move(current_value, adj_value):
                queue.put((distance + 1, adj_position))
                visited_positions.add(adj_position)

    return -1

def get_first(lines):
    map = [list(line) for line in lines]
    start_position = next(iter_positions_by_value(map, value='S'))
    end_position = next(iter_positions_by_value(map, value='E'))

    map[start_position.x][start_position.y] = 'a'
    map[end_position.x][end_position.y] = 'z'

    return get_min_distance(
        map,
        start_position,
        {end_position},
        is_accepted_move=lambda current, next: ord(current) + 1 >= ord(next),
    )

def get_second(lines):
    map = [list(line.replace('S', 'a')) for line in lines]
    start_position = next(iter_positions_by_value(map, value='E'))
    end_positions = set(iter_positions_by_value(map, value='a'))

    map[start_position.x][start_position.y] = 'z'

    return get_min_distance(
        map,
        start_position,
        end_positions,
        is_accepted_move=lambda current, next: ord(next) + 1 >= ord(current),
    )

if __name__ == '__main__':
    run(get_first, get_second)
