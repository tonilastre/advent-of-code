from collections import namedtuple
from typing import Dict, Iterator, Set
from queue import PriorityQueue
from aoc import run

Range = namedtuple('Range', 'start, end')
Point = namedtuple('Point', 'x, y')

EMPTY = '.'
ROCK = '#'

class Wind:
    DIRECTION_BY_WIND = {
        '^': Point(-1, 0),
        '>': Point(0, 1),
        'v': Point(1, 0),
        '<': Point(0, -1),
    }

    def __init__(self, start_point: Point, direction: Point, range: Range):
        self.start_point = start_point
        self.direction = direction
        self.range = Range(min(range.start, range.end), max(range.start, range.end))

    def get_point_by_step(self, step: int = 0) -> Point:
        dx, dy = self.direction
        range_len = self.range.end - self.range.start
        new_x = self.start_point.x + dx * step
        new_y = self.start_point.y + dy * step

        if dx == 0:
            new_y = self.range.start + (new_y - self.range.start) % range_len
        else:
            new_x = self.range.start + (new_x - self.range.start) % range_len

        return Point(new_x, new_y)

    @staticmethod
    def iter_winds(map: Dict[Point, str]) -> Iterator['Wind']:
        range_y = get_range_y(map)
        range_x = get_range_x(map)

        for point, value in map.items():
            direction = Wind.DIRECTION_BY_WIND.get(value)
            if direction is None:
                continue
            range = Range(1, (range_y.end if direction.x == 0 else range_x.end) - 1)
            yield Wind(point, direction, range)

def read_input_lines(lines) -> Dict[Point, str]:
    map = {}
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char != EMPTY:
                map[Point(x, y)] = char
    return map

def get_range_x(map: Dict[Point, str]) -> Range:
    return Range(min(x for x, _ in map), max(x for x, _ in map) + 1)

def get_range_y(map: Dict[Point, str]) -> Range:
    return Range(min(y for _, y in map), max(y for _, y in map) + 1)

def get_start_point(map: Dict[Point, str]) -> Point:
    min_y, max_y = get_range_y(map)
    target_x, _ = get_range_x(map)

    target_y = next(y for y in range(min_y, max_y) if Point(target_x, y) not in map)
    return Point(target_x, target_y)

def get_end_point(map: Dict[Point, str]) -> Point:
    min_y, max_y = get_range_y(map)
    _, target_x = get_range_x(map)

    target_y = next(y for y in range(min_y, max_y) if Point(target_x - 1, y) not in map)
    return Point(target_x - 1, target_y)

def iter_adj_points(point: Point, range_x: Range, range_y: Range) -> Iterator[Point]:
    for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        x = point.x + dx
        y = point.y + dy

        if range_x.start <= x < range_x.end and range_y.start <= y < range_y.end:
            yield Point(x, y)

def find_min_steps(map, start_point: Point, end_point: Point, start_step: int = 0) -> int:
    range_y = get_range_y(map)
    range_x = get_range_x(map)

    wall_points: Set[Point] = set(point for point, value in map.items() if value == ROCK)
    winds = list(Wind.iter_winds(map))
    wind_points_by_step: Dict[int, Set[Point]] = {}

    queue = PriorityQueue()
    queue.put((start_step, start_point))
    visited = set()

    while not queue.empty():
        iteration = queue.get()

        if iteration in visited:
            continue
        visited.add(iteration)

        step, point = iteration
        if point == end_point:
            return step

        step += 1

        if step not in wind_points_by_step:
            wind_points_by_step[step] = set(wind.get_point_by_step(step) for wind in winds)
        wind_points = wind_points_by_step[step]

        if point not in wind_points:
            queue.put((step, point))

        for adj_point in iter_adj_points(point, range_x, range_y):
            if adj_point not in wall_points and adj_point not in wind_points:
                queue.put((step, adj_point))

    return -1

def get_first(lines):
    map = read_input_lines(lines)
    start_point = get_start_point(map)
    end_point = get_end_point(map)

    return find_min_steps(map, start_point, end_point)

def get_second(lines):
    map = read_input_lines(lines)
    start_point = get_start_point(map)
    end_point = get_end_point(map)

    steps1 = find_min_steps(map, start_point, end_point)
    steps2 = find_min_steps(map, end_point, start_point, start_step=steps1)
    return find_min_steps(map, start_point, end_point, start_step=steps2)

if __name__ == '__main__':
    run(get_first, get_second)
