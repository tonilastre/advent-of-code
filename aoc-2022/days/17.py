from math import floor, ceil
from typing import List, Set, Tuple, Optional, Iterable
from aoc import run

PositionType = Tuple[int, int]
ShapeType = Iterable[PositionType]

WIDTH = 7
INIT_X_DIFF = 2
INIT_Y_DIFF = 3

SHAPES = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],           # -
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],   # +
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],   # L (reverse)
    [(0, 0), (0, 1), (0, 2), (0, 3)],           # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],           # (box)
]

SHAPE_WIDTHS = [max(x for x, _ in shape) + 1 for shape in SHAPES]

def parse_input_line(line: str) -> List[int]:
    return [-1 if l == '<' else 1 for l in line]

def get_translated_shape(shape: ShapeType, position: PositionType) -> ShapeType:
    x, y = position
    return [(sx + x, sy + y) for sx, sy in shape]

def can_shape_move(map: Set[PositionType], new_shape: ShapeType) -> bool:
    if not all(0 <= x < WIDTH for x, _ in new_shape):
        return False
    return all(point not in map for point in new_shape)

def find_cycle(array) -> Optional[Tuple[int, int]]:
    # Floyd's cycle-finding algorithm
    if len(array) <= 3:
        return None

    slow_pointer = 1
    fast_pointer = 2

    while array[slow_pointer] != array[fast_pointer]:
        slow_pointer += 1
        fast_pointer += 2
        if fast_pointer >= len(array):
            return None

    cycle_start_index = 0
    slow_pointer = 0
    while array[slow_pointer] != array[fast_pointer]:
        slow_pointer += 1
        fast_pointer += 1
        cycle_start_index += 1
        if fast_pointer >= len(array):
            return None

    cycle_len = 1
    fast_pointer = slow_pointer + 1
    while array[slow_pointer] != array[fast_pointer]:
        fast_pointer += 1
        cycle_len += 1
        if fast_pointer >= len(array):
            return None

    return cycle_start_index, cycle_len

def get_max_height(tilts: List[int], n: int) -> int:
    map: Set[PositionType] = {(x, -1) for x in range(WIDTH)}

    shape_index = 0
    shapes_len = len(SHAPES)
    tilt_index = 0
    tilts_len = len(tilts)

    max_height = 0
    last_max_height = 0

    # Contains (height diff, ending tilt index) for each group
    # of completed sizes (e.g. 0, 5, 10, ... - for size length of 5)
    shape_iterations: List[Tuple[int, int]] = []
    is_cycle_found = False
    cycle_shape_iteration = -1
    cycle_start_index = -1
    cycle_len = -1

    shape_count = 0
    while shape_count < n:
        if shape_index == 0 and shape_count > 0:
            shape_iterations.append((max_height - last_max_height, tilt_index))
            last_max_height = max_height

            if not is_cycle_found:
                cycle = find_cycle(shape_iterations)
                if cycle is not None:
                    cycle_start_index, cycle_len = cycle
                    is_cycle_found = True
                    # Index of the shape iteration when the cycle repetition can be used
                    cycle_shape_iteration = cycle_start_index + ceil((shape_count - cycle_start_index)/cycle_len) * cycle_len

            if is_cycle_found and len(shape_iterations) == cycle_shape_iteration:
                remaining_cycles = floor((n - shape_count)/(cycle_len * shapes_len))
                cycle_sum = sum(
                    height_diff for height_diff, _ in shape_iterations[cycle_start_index:cycle_start_index + cycle_len]
                )

                shape_count += remaining_cycles * shapes_len * cycle_len
                tilt_index = shape_iterations[cycle_start_index - 1][1]
                max_height += remaining_cycles * cycle_sum
                map = set(get_translated_shape(map, (0, remaining_cycles * cycle_sum)))

                if shape_count >= n:
                    break

        shape = SHAPES[shape_index]
        shape_width = SHAPE_WIDTHS[shape_index]
        shape_index = (shape_index + 1) % shapes_len

        shape_x = INIT_X_DIFF
        shape_max_x = WIDTH - shape_width

        # Initial pushes with clear map below
        for _ in range(INIT_Y_DIFF + 1):
            x = tilts[tilt_index]
            tilt_index = (tilt_index + 1) % tilts_len
            if 0 <= shape_x + x <= shape_max_x:
                shape_x += x

        shape = get_translated_shape(shape, (shape_x, max_height))

        while True:
            down_shape = get_translated_shape(shape, (0, -1))
            if not can_shape_move(map, down_shape):
                map.update(shape)
                max_height = max(max_height, *(y + 1 for _, y in shape))
                break

            shape = down_shape

            x = tilts[tilt_index]
            tilt_index = (tilt_index + 1) % tilts_len
            side_shape = get_translated_shape(shape, (x, 0))
            if can_shape_move(map, side_shape):
                shape = side_shape

        shape_count += 1

    return max_height

def get_first(lines):
    tilts = parse_input_line(lines[0])
    return get_max_height(tilts, n=2022)

def get_second(lines):
    tilts = parse_input_line(lines[0])
    return get_max_height(tilts, n=1_000_000_000_000)

if __name__ == '__main__':
    run(get_first, get_second)
