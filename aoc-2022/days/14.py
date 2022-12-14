from typing import Iterator
from collections import defaultdict, namedtuple
from aoc import run, get_int_numbers, pairwise, sign, batch

ROCK = '#'
SAND = 'o'
AIR = '.'

Point = namedtuple('Point', 'x, y')

def iter_line_points(start: Point, end: Point) -> Iterator[Point]:
    dx = sign(end.x - start.x)
    dy = sign(end.y - start.y)

    current = start
    while True:
        yield current
        if current == end:
            break
        current = Point(current.x + dx, current.y + dy)

def parse_input_as_map(lines):
    map = {}
    for line in lines:
        numbers = get_int_numbers(line)
        points = (Point(x, y) for (x, y) in batch(numbers, batch_size=2))
        for start, end in pairwise(points):
            for point in iter_line_points(start, end):
                map[point] = ROCK
    return map

def print_map(map):
    min_x = min(x for x, _ in map.keys())
    max_x = max(x for x, _ in map.keys())
    min_y = min(y for _, y in map.keys())
    max_y = max(y for _, y in map.keys())

    for y in range(min_y, max_y + 1):
        print(''.join(map.get((x, y)) or AIR for x in range(min_x, max_x + 1)))

def get_top_ys_by_x(map):
    top_ys_by_x = defaultdict(set)
    for (x, y) in map.keys():
        if (x, y - 1) not in map:
            top_ys_by_x[x].add(y - 1)
    return top_ys_by_x

def get_top_point(top_ys_by_x, source):
    top_ys = top_ys_by_x.get(source.x)
    if not top_ys:
        return None

    y = min((top_y for top_y in top_ys if top_y >= source.y), default=-1)
    return Point(source.x, y) if y != -1 else None

def simulate_sand(map, sand_source: Point):
    source = sand_source
    # Holds `y` per column (x) where sand can land
    top_ys_by_x = get_top_ys_by_x(map)

    # Uncomment for printing the source out
    # map[sand_source] = '+'

    while True:
        top_point = get_top_point(top_ys_by_x, source)
        if not top_point:
            break

        left_down_point = Point(top_point.x - 1, top_point.y + 1)
        right_down_point = Point(top_point.x + 1, top_point.y + 1)

        if not map.get(left_down_point):
            source = left_down_point
            continue

        if not map.get(right_down_point):
            source = right_down_point
            continue

        map[top_point] = SAND
        if top_point == sand_source:
            break

        # As sand landed, update with the new available `y`
        tops = top_ys_by_x[top_point.x]
        tops.remove(top_point.y)
        tops.add(top_point.y - 1)

        source = sand_source

def get_first(lines):
    map = parse_input_as_map(lines)
    sand_source = Point(500, 0)

    simulate_sand(map, sand_source=sand_source)
    return sum(1 for v in map.values() if v == SAND)

def get_second(lines):
    map = parse_input_as_map(lines)
    sand_source = Point(500, 0)

    max_y = max(y for _, y in map.keys()) + 2
    start_baseline = Point(sand_source.x - max_y, max_y)
    end_baseline = Point(sand_source.x + max_y, max_y)

    for point in iter_line_points(start_baseline, end_baseline):
        map[point] = ROCK

    simulate_sand(map, sand_source=sand_source)
    return sum(1 for v in map.values() if v == SAND)

if __name__ == '__main__':
    run(get_first, get_second)
