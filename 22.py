from aoc import run, get_int_numbers
from typing import List, Optional, Iterator, Tuple
from operator import mul
from functools import reduce
from collections import namedtuple

Cuboid = namedtuple('Cuboid', 'rx, ry, rz')

class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __len__(self):
        return abs(self.end - self.start)

    def is_within(self, range: 'Range') -> bool:
        return range.start <= self.start and self.end <= range.end

    def is_disjoint(self, range: 'Range') -> bool:
        """Returns if two ranges share any items"""
        return range.end <= self.start or self.end <= range.start

    def intersection(self, range: 'Range') -> Optional['Range']:
        """Returns a range that is part of both ranges"""
        if self.is_disjoint(range):
            return None

        new_start = max(self.start, range.start)
        new_end = min(self.end, range.end)
        return Range(new_start, new_end)

    def difference(self, range: 'Range') -> List['Range']:
        """Returns a list of ranges that are present in self range but not in both ranges"""
        if self.is_disjoint(range):
            return [copy(self)]

        # Range is covering the first part
        if range.start <= self.start and self.start < range.end < self.end:
            return [Range(range.end, self.end)]

        # Range is covering the second part
        if self.start < range.start < self.end and self.end <= range.end:
            return [Range(self.start, range.start)]

        # Range is inside the self
        if self.start < range.start < self.end and self.start < range.end < self.end:
            return [Range(self.start, range.start), Range(range.end, self.end)]

        return []

    def __eq__(self, other: 'Range') -> bool:
        return self.start == other.start and self.end == other.end

    def __copy__(self) -> 'Range':
        return Range(self.start, self.end)

    def __str__(self) -> str:
        return f'[{self.start}, {self.end}>'

    def __repr__(self) -> str:
        return str(self)

def iter_parsed_input(lines):
    for line in lines:
        is_on = line.startswith('on')
        numbers = get_int_numbers(line)
        yield is_on, Cuboid(*(
            Range(numbers[i * 2], numbers[i * 2 + 1] + 1) for i in range(3)
        ))

def is_cuboid_in_range(cuboid: Cuboid, range: Range) -> bool:
    return all(r.is_within(range) for r in cuboid)

def is_cuboid_disjoint(c1: Cuboid, c2: Cuboid) -> bool:
    return any(r1.is_disjoint(r2) for r1, r2 in zip(c1, c2))

def get_cuboid_len(cuboid: Cuboid) -> int:
    return reduce(mul, (len(r) for r in cuboid))

def iter_cuboid_difference(c1: Cuboid, c2: Cuboid) -> Iterator[Cuboid]:
    """Returns all cuboids that are present in c1 but not in both c1 and c2"""
    # Difference of range X has full Y and Z ranges
    for diff_rx in c1.rx.difference(c2.rx):
        yield Cuboid(diff_rx, c1.ry, c1.rz)

    intersect_rx = c1.rx.intersection(c2.rx)
    if not intersect_rx:
        return

    # Difference of range Y has full Z ranges within intersected X range
    for diff_ry in c1.ry.difference(c2.ry):
        yield Cuboid(intersect_rx, diff_ry, c1.rz)

    intersect_ry = c1.ry.intersection(c2.ry)
    if not intersect_ry:
        return

    # Difference of range Z is within intersected X and Y ranges
    for diff_rz in c1.rz.difference(c2.rz):
        yield Cuboid(intersect_rx, intersect_ry, diff_rz)

def activate_cuboid(cuboids: List[Cuboid], active_cuboid: Cuboid) -> List[Cuboid]:
    for cuboid in cuboids:
        if is_cuboid_disjoint(cuboid, active_cuboid):
            continue

        current_cuboids = list(cuboids)
        for new_active_cuboid in iter_cuboid_difference(active_cuboid, cuboid):
            current_cuboids = activate_cuboid(current_cuboids, new_active_cuboid)
        return current_cuboids

    return list(cuboids) + [active_cuboid]

def deactivate_cuboid(cuboids: List[Cuboid], inactive_cuboid: Cuboid) -> List[Cuboid]:
    new_active_cuboids = []
    for cuboid in cuboids:
        if is_cuboid_disjoint(cuboid, inactive_cuboid):
            new_active_cuboids.append(cuboid)
            continue

        for new_active_cuboid in iter_cuboid_difference(cuboid, inactive_cuboid):
            new_active_cuboids.append(new_active_cuboid)

    return new_active_cuboids

def get_active_cuboids_count(inputs: Tuple[bool, Cuboid], range: Optional[Range] = None):
    cuboids = []
    for is_cuboid_active, cuboid in inputs:
        if range and not is_cuboid_in_range(cuboid, range):
            continue

        if is_cuboid_active:
            cuboids = activate_cuboid(cuboids, cuboid)
        else:
            cuboids = deactivate_cuboid(cuboids, cuboid)

    return sum(get_cuboid_len(c) for c in cuboids)

def get_first(lines):
    inputs = list(iter_parsed_input(lines))
    return get_active_cuboids_count(inputs, range = Range(-50, 51))

def get_second(lines):
    inputs = list(iter_parsed_input(lines))
    return get_active_cuboids_count(inputs)

if __name__ == '__main__':
    run(get_first, get_second)