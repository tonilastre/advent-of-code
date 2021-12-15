from aoc import run
from queue import PriorityQueue

def iter_adj_positions(matrix, position):
    i, j = position
    for new_i, new_j in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
        if new_i < 0 or new_i >= len(matrix):
            continue
        if new_j < 0 or new_j >= len(matrix[i]):
            continue
        yield (new_i, new_j)

def expand_matrix(matrix, n):
    new_matrix = []
    get_cell_value = lambda v: v if v < 10 else v - 9

    for start in range(n):
        for row in matrix:
            new_row = []
            for i in range(start, start + n):
                new_row.extend([get_cell_value(v + i) for v in row])
            new_matrix.append(new_row)

    return new_matrix

def get_distances(matrix):
    start_position = (0, 0)
    distances = dict({ start_position: 0 })
    visited_positions = set()

    queue = PriorityQueue()
    queue.put((0, start_position))

    while not queue.empty():
        (distance, position) = queue.get()
        visited_positions.add(position)

        for adj_position in iter_adj_positions(matrix, position):
            if adj_position in visited_positions:
                continue

            old_distance = distances.get(adj_position)
            new_distance = distance + matrix[adj_position[0]][adj_position[1]]
            if old_distance is None or new_distance < old_distance:
                distances[adj_position] = new_distance
                queue.put((new_distance, adj_position))

    return distances

def get_last_position(matrix):
    return len(matrix) - 1, len(matrix[0]) - 1

def get_first(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    distances = get_distances(matrix)
    return distances[get_last_position(matrix)]

def get_second(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    expanded_matrix = expand_matrix(matrix, n = 5)
    distances = get_distances(expanded_matrix)
    return distances[get_last_position(expanded_matrix)]

if __name__ == '__main__':
    run(get_first, get_second)
