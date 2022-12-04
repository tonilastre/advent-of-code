from collections import namedtuple
from aoc import run, get_int_numbers

Range = namedtuple('Range', 'start, end')

def parse_input(line):
    start1, end1, start2, end2 = get_int_numbers(line, only_positive=True)
    return Range(start1, end1), Range(start2, end2)

def includes_range(range1, range2):
    return range1.start <= range2.start <= range1.end and range1.start <= range2.end <= range1.end

def overlaps_range(range1, range2):
    return not(range1.end < range2.start or range1.start > range2.end)

def get_first(lines):
    range_pairs = [parse_input(line) for line in lines]
    return sum(int(includes_range(r1, r2) or includes_range(r2, r1)) for r1, r2 in range_pairs)

def get_second(lines):
    range_pairs = [parse_input(line) for line in lines]
    return sum(int(overlaps_range(r1, r2)) for r1, r2 in range_pairs)

if __name__ == '__main__':
    run(get_first, get_second)
