from typing import Iterable, Tuple, Iterator, Optional, Set
from itertools import cycle, product
from collections import namedtuple, defaultdict
from aoc import run

Point = namedtuple('Point', 'x, y')

DIRECTIONS = [Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)]

def parse_input_lines(lines) -> Iterator[Point]:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                yield Point(x, y)

def get_range_x(points: Iterable[Point]) -> Tuple[int, int]:
    return min(x for x, _ in points), max(x for x, _ in points) + 1

def get_range_y(points: Iterable[Point]) -> Tuple[int, int]:
    return min(y for _, y in points), max(y for _, y in points) + 1

def get_adj_points(point: Point, direction: Optional[Point] = None) -> Iterator[Point]:
    x, y = point
    if direction:
        dx, dy = direction
        yield Point(x + (-1 if dx == 0 else dx), y + (-1 if dy == 0 else dy))
        yield Point(x + dx, y + dy)
        yield Point(x + (1 if dx == 0 else dx), y + (1 if dy == 0 else dy))
        return

    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        yield Point(x + dx, y + dy)

def print_points(points: Iterable[Point]) -> None:
    min_x, max_x = get_range_x(points)
    min_y, max_y = get_range_y(points)

    for y in range(min_y, max_y):
        print(''.join('#' if Point(x, y) in points else '.' for x in range(min_x, max_x)))

def is_adj_empty(point: Point, points: Set[Point]) -> bool:
    return all(adj_point not in points for adj_point in get_adj_points(point))

def simulate(points: Iterable[Point], directions: Iterable[Point], max_rounds: int = None) -> Tuple[int, Iterable[Point]]:
    dir_index = 0
    round = 0

    while True:
        round += 1
        if max_rounds is not None and round > max_rounds:
            break

        new_points = list(points)
        unique_points = set(points)

        for i, point in enumerate(points):
            # Stay as is because adj points are empty
            if is_adj_empty(point, unique_points):
                continue

            # Check available direction and propose new position
            for dir_diff in range(len(directions)):
                direction = directions[(dir_index + dir_diff) % len(directions)]
                if all(adj_point not in unique_points for adj_point in get_adj_points(point, direction)):
                    new_points[i] = Point(point.x + direction.x, point.y + direction.y)
                    break

        count_by_point = defaultdict(int)
        for new_point in new_points:
            count_by_point[new_point] += 1

        move_count = 0
        for i, new_point in enumerate(new_points):
            if count_by_point[new_point] != 1:
                continue

            if new_point != points[i]:
                points[i] = new_point
                move_count += 1

        if move_count == 0:
            break

        dir_index = (dir_index + 1) % len(directions)

    return round, points

def get_first(lines):
    points = list(parse_input_lines(lines))
    _, points = simulate(points, directions=DIRECTIONS, max_rounds=10)
    min_x, max_x = get_range_x(points)
    min_y, max_y = get_range_y(points)
    size = (max_x - min_x) * (max_y - min_y)
    return size - len(points)

def get_second(lines):
    points = list(parse_input_lines(lines))
    rounds, _ = simulate(points, directions=DIRECTIONS)
    return rounds

if __name__ == '__main__':
    run(get_first, get_second)
