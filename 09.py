from aoc import run
from queue import SimpleQueue
from functools import reduce
from collections import namedtuple

def enumerate_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            yield (i, j), matrix[i][j]

def iter_adj_positions(position):
    i, j = position
    yield from ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))

def get_point(matrix, position, default_value = 10):
    i, j = position
    if i < 0 or i >= len(matrix):
        return default_value
    if j < 0 or j >= len(matrix[i]):
        return default_value
    return matrix[i][j]

def iter_lowest_points(matrix):
    for position, point in enumerate_matrix(matrix):
        if all(point < get_point(matrix, p) for p in iter_adj_positions(position)):
            yield point

def get_basin_size(matrix, position, matrix_is_visited):
    queue = SimpleQueue()
    queue.put(position)
    basin_size = 0

    while not queue.empty():
        new_position = queue.get()
        if get_point(matrix_is_visited, new_position, default_value=True):
            continue

        matrix_is_visited[new_position[0]][new_position[1]] = True
        basin_size += 1

        for adj_position in iter_adj_positions(new_position):
            queue.put(adj_position)

    return basin_size

def iter_basin_sizes(matrix):
    basin_sizes = []
    matrix_is_visited = [[cell >= 9 for cell in row] for row in matrix]

    for position, _ in enumerate_matrix(matrix):
        if not get_point(matrix_is_visited, position, default_value=True):
            yield get_basin_size(matrix, position, matrix_is_visited)

def get_first(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    return sum(point + 1 for point in iter_lowest_points(matrix))

def get_second(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    basin_sizes = list(sorted(iter_basin_sizes(matrix), reverse=True))
    return reduce(lambda x, y: x * y, basin_sizes[:3])

if __name__ == '__main__':
    run(get_first, get_second)
