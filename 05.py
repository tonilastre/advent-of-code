import sys
from collections import defaultdict, namedtuple
from itertools import combinations
from aoc import get_int_numbers, run

Point = namedtuple('Point', 'x, y')
Line = namedtuple('Line', 'x1, y1, x2, y2')

def parse_input(inp):
    x1, y1, x2, y2 = get_int_numbers(inp)
    return Line(x1, y1, x2, y2)

def get_delta(start, end):
    if start == end:
        return 0
    return 1 if start < end else -1

def get_cross_points_count(lines):
    canvas = defaultdict(int)

    for line in lines:
        dx = get_delta(line.x1, line.x2)
        dy = get_delta(line.y1, line.y2)

        point = Point(line.x1, line.y1)
        canvas[point] += 1

        while point != Point(line.x2, line.y2):
            point = Point(point.x + dx, point.y + dy)
            canvas[point] += 1

    return sum(cell > 1 for cell in canvas.values())

def get_first(lines):
    lines = [parse_input(l.strip()) for l in lines]
    straight_lines = [l for l in lines if l.x1 == l.x2 or l.y1 == l.y2]
    return get_cross_points_count(straight_lines)

def get_second(lines):
    lines = [parse_input(l.strip()) for l in lines]
    return get_cross_points_count(lines)

if __name__ == '__main__':
    run(get_first, get_second)
