from typing import List, Tuple
from functools import lru_cache
from collections import namedtuple
from aoc import run, get_int_numbers

Point = namedtuple('Point', 'x, y')
Range = namedtuple('Range', 'start, end')

@lru_cache
def get_manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def parse_input_line(line: str) -> Tuple[Point, Point]:
    numbers = get_int_numbers(line)
    return Point(*numbers[:2]), Point(*numbers[2:])

def is_overlapping_range(range1: Range, range2: Range) -> bool:
    return not(range1.end < range2.start or range2.end < range1.start)

def merge_ranges(ranges: List[Range], new_range: Range) -> List[Range]:
    merged_ranges = []
    overlapping_ranges = [new_range]

    for range in ranges:
        if is_overlapping_range(range, new_range):
            overlapping_ranges.append(range)
            continue
        merged_ranges.append(range)

    merged_ranges.append(Range(
        min(r.start for r in overlapping_ranges),
        max(r.end for r in overlapping_ranges),
    ))
    return sorted(merged_ranges)

def remove_ranges(range: Range, removable_ranges: List[Range]) -> List[Range]:
    ranges = [range]

    for removable_range in removable_ranges:
        new_ranges = []
        for range in ranges:
            if not is_overlapping_range(range, removable_range):
                new_ranges.append(range)
                continue

            if range.start < removable_range.start and range.end <= removable_range.end:
                new_ranges.append(Range(range.start, removable_range.start))
                continue

            if removable_range.start <= range.start and removable_range.end < range.end:
                new_ranges.append(Range(removable_range.end, range.end))
                continue

            if range.start < removable_range.start and removable_range.end < range.end:
                new_ranges.append(Range(range.start, removable_range.start))
                new_ranges.append(Range(removable_range.end, range.end))
                continue

        ranges = new_ranges

    return ranges

def get_signal_ranges(pairs: Tuple[Point, Point], target_y: int) -> List[Range]:
    ranges = []

    for sensor, beacon in pairs:
        d = get_manhattan_distance(sensor, beacon)
        offset_x = d - abs(sensor.y - target_y)

        if offset_x >= 0:
            ranges = merge_ranges(ranges, Range(sensor.x - offset_x, sensor.x + offset_x + 1))

    return ranges

def get_first(lines):
    pairs = [parse_input_line(line) for line in lines]
    target_y = 2_000_000

    ranges = get_signal_ranges(pairs, target_y=target_y)
    range_len = sum(r.end - r.start for r in ranges)

    beacons_x = {b.x for _, b in pairs if b.y == target_y}
    beacon_count = sum(any(r.start <= x < r.end for r in ranges) for x in beacons_x)

    return range_len - beacon_count

def get_second(lines):
    pairs = [parse_input_line(line) for line in lines]
    min_value = 0
    max_value = 4_000_000

    range_x = Range(min_value, max_value + 1)

    for y in range(min_value, max_value + 1):
        ranges = get_signal_ranges(pairs, target_y=y)
        available_ranges = remove_ranges(range_x, ranges)
        if not len(available_ranges):
            continue

        x = available_ranges[0].start
        return x * max_value + y

    return 0

if __name__ == '__main__':
    run(get_first, get_second)
