from aoc import run, get_int_numbers
from collections import namedtuple
from typing import Iterator, List, Dict, Set

Point2D = namedtuple('Point2D', 'x, y')
Point3D = namedtuple('Point3D', 'x, y, z')
Block = namedtuple('Block', 'start, end')
RefPoint1D = namedtuple('RefPoint1D', 'z, block_index')

class Block:
    def __init__(self, start: Point3D, end: Point3D):
        self.start = start
        self.end = end
        self.min_x = min(self.start.x, self.end.x)
        self.max_x = max(self.start.x, self.end.x)
        self.min_y = min(self.start.y, self.end.y)
        self.max_y = max(self.start.y, self.end.y)
        self.min_z = min(self.start.z, self.end.z)
        self.max_z = max(self.start.z, self.end.z)

    def iter_points(self) -> Iterator[Point3D]:
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                for z in range(self.min_z, self.max_z + 1):
                    yield Point3D(x, y, z)

    def get_z_diff(self) -> int:
        return self.max_z - self.min_z + 1

def parse_line(line) -> Block:
    numbers = get_int_numbers(line)
    return Block(Point3D(*numbers[:3]), Point3D(*numbers[3:]))

def get_dependencies(blocks: List[Block]) -> List[Set[int]]:
    blocks = sorted(blocks, key=lambda b: b.min_z)
    max_ref_by_xy: Dict[Point2D, RefPoint1D] = dict()
    dependencies: List[Set[int]] = []

    for i, block in enumerate(blocks):
        points = list(block.iter_points())
        max_z = 0
        block_index_dependencies: Set[int] = set()
        for point in points:
            xy = Point2D(point.x, point.y)
            ref = max_ref_by_xy.get(xy)
            if ref is None:
                continue
            if ref.z == max_z:
                block_index_dependencies.add(ref.block_index)
            elif ref.z > max_z:
                max_z = ref.z
                block_index_dependencies = set([ref.block_index])

        dependencies.append(block_index_dependencies)
        for point in points:
            xy = Point2D(point.x, point.y)
            max_ref_by_xy[xy] = RefPoint1D(max_z + block.get_z_diff(), i)

    return dependencies

def get_dependent_blocks_indexes(dependencies: List[Set[int]]) -> List[int]:
    indexes: Set[int] = set()
    for block_indexes in dependencies:
        if len(block_indexes) == 1:
            indexes.update(block_indexes)
    return sorted(indexes)

def get_first(lines):
    blocks = [parse_line(line) for line in lines]
    dependencies = get_dependencies(blocks)
    dependent_block_indexes = get_dependent_blocks_indexes(dependencies)
    return len(blocks) - len(dependent_block_indexes)

def get_second(lines):
    blocks = [parse_line(line) for line in lines]
    dependencies = get_dependencies(blocks)
    dependent_block_indexes = get_dependent_blocks_indexes(dependencies)

    collapsed_block_counts: List[int] = []
    for block_index in dependent_block_indexes:
        collapsed_indexes = set([block_index])
        is_collapse_updated = False
        while not is_collapse_updated:
            is_collapse_updated = False
            for i, indexes in enumerate(dependencies):
                if not indexes:
                    continue
                if indexes.issubset(collapsed_indexes):
                    collapsed_indexes.add(i)
                    is_collapse_updated = True
        collapsed_block_counts.append(len(collapsed_indexes) - 1)

    return sum(collapsed_block_counts)

if __name__ == '__main__':
    run(get_first, get_second)
