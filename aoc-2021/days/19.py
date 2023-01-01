from aoc import run, get_int_numbers
from typing import Iterator, Iterable, List, Set
from collections import namedtuple
from itertools import product, permutations

Scanner = namedtuple('Scanner', 'index, points')
Point = namedtuple('Point', 'x, y, z')
Rotation = namedtuple('Rotation', 'rx, ry, rz')
Translation = namedtuple('Translation', 'dx, dy, dz')

MIN_COMMON_POINTS = 12
PIVOT_POSITION = Point(0, 0, 0)

class Scanner:
    def __init__(self, index):
        self.index = index
        self.points = []
        self.beacons = None
        self.position = None

    def calibrate_as_pivot(self):
        self.position = PIVOT_POSITION
        self.beacons = set(self.points)

    def is_calibrated(self):
        return self.position is not None

    def calibrate(self, other_scanner):
        for rotation in iter_rotations():
            rotated_points = [apply_rotation(p, rotation) for p in self.points]
            for translation in iter_translations(rotated_points[:-MIN_COMMON_POINTS-1], other_scanner.beacons):
                translated_beacon_points = set(apply_translation(p, translation) for p in rotated_points)

                intersected_beacon_points = other_scanner.beacons.intersection(translated_beacon_points)
                if len(intersected_beacon_points) < MIN_COMMON_POINTS:
                    continue

                self.position = apply_translation(PIVOT_POSITION, translation)
                self.beacons = translated_beacon_points
                return

def get_input_as_scanners(lines) -> List[Scanner]:
    scanners = []

    for line in lines:
        if not line:
            continue
        if 'scanner' in line:
            scanner_index = get_int_numbers(line)[0]
            scanners.append(Scanner(scanner_index))
            continue
        scanners[-1].points.append(Point(*get_int_numbers(line)))

    return scanners

def get_manhattan_distance(point1: Point, point2: Point) -> int:
    return sum(map(abs, get_translation(point1, point2)))

def iter_translations(points1: Iterable[Point], points2: Iterable[Point]):
    for point1 in points1:
        for point2 in points2:
            yield get_translation(point2, point1)

def iter_rotations() -> Iterator[Rotation]:
    for index_moves in permutations([1, 2, 3]):
        for direction_moves in product([1, -1], repeat=3):
            yield Rotation(*(i * d for i, d in zip(index_moves, direction_moves)))

def get_translation(point1: Point, point2: Point) -> Translation:
    return Translation(*(value1 - value2 for value1, value2 in zip(point1, point2)))

def apply_translation(point: Point, translation: Translation) -> Point:
    return Point(*(value1 + value2 for value1, value2 in zip(point, translation)))

def apply_rotation(point: Point, rotation: Rotation) -> Point:
    coordinates = []
    for rotation_value in rotation:
        value = point[abs(rotation_value) - 1]
        value = value * -1 if rotation_value < 0 else value
        coordinates.append(value)
    return Point(*coordinates)

def get_calibrated_scanners(scanners):
    scanners[0].calibrate_as_pivot()

    calibrated_scanners = [scanners[0]]
    uncalibrated_scanners = scanners[1:]
    checked_scanner_index_pairs = set()

    while uncalibrated_scanners:
        scanner = uncalibrated_scanners.pop(0)

        for calibrated_scanner in calibrated_scanners:
            scanner_index_pair = (scanner.index, calibrated_scanner.index)
            if scanner_index_pair in checked_scanner_index_pairs:
                continue

            checked_scanner_index_pairs.add(scanner_index_pair)
            scanner.calibrate(calibrated_scanner)
            # print(f'Checking {scanner.index:02} - {calibrated_scanner.index:02} {"(calibrated)" if scanner.is_calibrated() else ""}')
            if scanner.is_calibrated():
                calibrated_scanners.append(scanner)
                break

        if not scanner.is_calibrated():
            uncalibrated_scanners.append(scanner)

    return calibrated_scanners

def get_first(lines):
    scanners = get_input_as_scanners(lines)
    calibrated_scanners = get_calibrated_scanners(scanners)

    all_beacons = set()
    for scanner in calibrated_scanners:
        all_beacons = all_beacons.union(scanner.beacons)
    return len(all_beacons)

def get_second(lines):
    scanners = get_input_as_scanners(lines)
    calibrated_scanners = get_calibrated_scanners(scanners)

    calibrated_scanner_pairs = product(calibrated_scanners, calibrated_scanners)
    return max(get_manhattan_distance(s1.position, s2.position) for s1, s2 in calibrated_scanner_pairs)

if __name__ == '__main__':
    run(get_first, get_second)
