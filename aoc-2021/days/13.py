from aoc import run
from collections import namedtuple

Point = namedtuple('Point', 'x, y')
Fold = namedtuple('Fold', 'axis, value')

def parse_input(lines):
    points = []
    folds = []
    for line in lines:
        if ',' in line:
            x, y = line.split(',')
            points.append(Point(int(x), int(y)))
        if 'fold along' in line:
            text, value = line.split('=')
            folds.append(Fold(text[-1], int(value)))
    return points, folds

def get_folded_points(points, fold):
    new_points = set()

    for point in points:
        new_x, new_y = point

        if fold.axis == 'x' and new_x > fold.value:
            new_x = 2 * fold.value - new_x
        if fold.axis == 'y' and new_y > fold.value:
            new_y = 2 * fold.value - new_y

        new_points.add(Point(new_x, new_y))

    return new_points

def print_points(points):
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    matrix = [[' '] * (max_x + 1) for _ in range(max_y + 1)]

    for p in points:
        matrix[p.y][p.x] = '#'

    print('\n'.join(''.join(row) for row in matrix))

def get_first(lines):
    points, folds = parse_input(lines)
    new_points = get_folded_points(points, folds[0])
    return len(new_points)

def get_second(lines):
    points, folds = parse_input(lines)
    for fold in folds:
        points = get_folded_points(points, fold)
    print_points(points)
    return 0

if __name__ == '__main__':
    run(get_first, get_second)
