from itertools import combinations
from queue import SimpleQueue
from typing import Set, Iterable
from collections import namedtuple, defaultdict
from aoc import run, get_int_numbers

Point = namedtuple('Point', 'x, y, z')

def parse_input_line(line: str) -> Point:
    return Point(*get_int_numbers(line))

def get_open_sides(points: Iterable[Point]) -> int:
    side_by_point = {p: 6 for p in points}

    for point1, point2 in combinations(points, 2):
        diff = sum(abs(c1 - c2) for c1, c2 in zip(point1, point2))
        if diff == 1:
            side_by_point[point1] -= 1
            side_by_point[point2] -= 1

    return sum(side_by_point.values())

def get_mid_points(points: Iterable[Point]) -> Set[Point]:
    mid_points: Set[Point] = set()
    for point1, point2 in combinations(points, 2):
        diffs = [abs(c1 - c2) for c1, c2 in zip(point1, point2) if c1 != c2]
        # Mid points have two equal coordinates and a distance on third (> 1)
        if len(diffs) != 1 and diffs[0] > 1:
            continue

        mid_point = Point(*((c1 + c2) // 2 for c1, c2 in zip(point1, point2)))
        mid_points.add(mid_point)
    return mid_points

def get_air_socket_points(points):
    coordinates_len = len(points[0])
    points = set(points)

    max_point = Point(*(max(p[i] for p in points) for i in range(coordinates_len)))
    min_point = Point(*(min(p[i] for p in points) for i in range(coordinates_len)))
    mid_points = get_mid_points(points)

    point_directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    air_socket_points: Set[Point] = set()

    while mid_points:
        mid_point = mid_points.pop()
        queue = SimpleQueue()
        queue.put(mid_point)
        visited_points: Set[Point] = set()

        area_points: Set[Point] = set()
        is_area_enclosed = True

        while not queue.empty():
            point = queue.get()
            # Remove unnecessary future checks
            if point in mid_points:
                mid_points.remove(point)

            if point in points or point in visited_points:
                continue

            visited_points.add(point)
            if not all(min_point[i] <= c <= max_point[i] for i, c in enumerate(point)):
                is_area_enclosed = False
                break

            area_points.add(point)
            for dx, dy, dz in point_directions:
                queue.put(Point(point.x + dx, point.y + dy, point.z + dz))

        if is_area_enclosed and area_points:
            air_socket_points.update(area_points)

    return air_socket_points

def get_first(lines):
    points = [parse_input_line(line) for line in lines]
    return get_open_sides(points)

def get_second(lines):
    points = [parse_input_line(line) for line in lines]
    air_socket_points = get_air_socket_points(points)
    return get_open_sides(points) - get_open_sides(air_socket_points)

if __name__ == '__main__':
    run(get_first, get_second)
