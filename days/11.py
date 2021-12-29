from aoc import run
from queue import SimpleQueue
from itertools import product

def enumerate_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            yield (i, j), matrix[i][j]

def iter_adj_positions(matrix, position):
    i, j = position
    for di, dj in product([-1, 0, 1], [-1, 0, 1]):
        new_i = i + di
        new_j = j + dj

        if new_i == i and new_j == j:
            continue
        if new_i < 0 or new_i >= len(matrix):
            continue
        if new_j < 0 or new_j >= len(matrix[i]):
            continue

        yield (new_i, new_j)

def get_flash_count(matrix):
    queue = SimpleQueue()

    # Single flashes
    for (i, j), _ in enumerate_matrix(matrix):
        matrix[i][j] += 1
        if matrix[i][j] == 10:
            queue.put((i, j))

    # Adjacent flashes
    while not queue.empty():
        i, j = queue.get()
        for adj_i, adj_j in iter_adj_positions(matrix, (i, j)):
            matrix[adj_i][adj_j] += 1
            if matrix[adj_i][adj_j] == 10:
                queue.put((adj_i, adj_j))

    # Resets
    flash_count = 0
    for (i, j), _ in enumerate_matrix(matrix):
        if matrix[i][j] >= 10:
            flash_count += 1
            matrix[i][j] = 0

    return flash_count

def get_first(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    return sum(get_flash_count(matrix) for _ in range(100))

def get_second(lines):
    matrix = [[int(l) for l in line if l] for line in lines]
    total_flashes = sum(len(r) for r in matrix)
    step = 1

    while True:
        flash_count = get_flash_count(matrix)
        if flash_count == total_flashes:
            break
        step += 1

    return step

if __name__ == '__main__':
    run(get_first, get_second)
