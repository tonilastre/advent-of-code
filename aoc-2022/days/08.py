from aoc import run
from functools import reduce

def parse_line(line):
    return [int(l) for l in line.strip()]

def iter_visible_matrix_row_positions(matrix):
    directions_j = (
        range(len(matrix[0])),
        range(len(matrix[0]) -1, -1, -1),
    )

    for i in range(len(matrix)):
        for direction_j in directions_j:
            max_j = -1
            for j in direction_j:
                if matrix[i][j] > max_j:
                    yield (i, j)
                max_j = max(matrix[i][j], max_j)

def iter_visible_matrix_column_positions(matrix):
    directions_i = (
        range(len(matrix)),
        range(len(matrix) -1, -1, -1),
    )

    for j in range(len(matrix[0])):
        for direction_i in directions_i:
            max_i = -1
            for i in direction_i:
                if matrix[i][j] > max_i:
                    yield (i, j)
                max_i = max(matrix[i][j], max_i)

def get_visibility_matrix(matrix):
    visibility = [[False] * len(row) for row in matrix]

    for i, j in iter_visible_matrix_row_positions(matrix):
        visibility[i][j] = True
    for i, j in iter_visible_matrix_column_positions(matrix):
        visibility[i][j] = True

    return visibility

def iter_all_adj_positions(matrix, position, movement):
    i, j = position
    di, dj = movement

    while True:
        i = i + di
        j = j + dj
        if not (0 <= i < len(matrix) and 0 <= j < len(matrix[i])):
            break
        yield (i, j)

def get_scenic_score(matrix, position):
    start_value = matrix[position[0]][position[1]]
    scores = []

    for movement in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        score = 0
        for i, j in iter_all_adj_positions(matrix, position, movement):
            score += 1
            if start_value <= matrix[i][j]:
                break
        scores.append(score)

    return reduce(lambda a, b: a * b, scores)

def get_max_scenic_score(matrix):
    max_score = 0
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            max_score = max(get_scenic_score(matrix, (i, j)), max_score)
    return max_score

def get_first(lines):
    matrix = [parse_line(l) for l in lines]
    visibility = get_visibility_matrix(matrix)
    return sum(sum(row) for row in visibility)

def get_second(lines):
    matrix = [parse_line(l) for l in lines]
    return get_max_scenic_score(matrix)

if __name__ == '__main__':
    run(get_first, get_second)
