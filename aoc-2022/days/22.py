from typing import List, Optional, Callable, Union, Tuple
from collections import defaultdict, namedtuple
from aoc import run

Point = namedtuple('Point', 'row, col')
Range = namedtuple('Range', 'start, end')
Line = namedtuple('Line', 'start, end')

class DirectionTurn:
    REVERSE = 'V'
    RIGHT = 'R'
    LEFT = 'L'
    REVERSE_TURN = 'T'
    KEEP = 'K'

    @staticmethod
    def get_new_direction(direction: Point, turn: str):
        if turn == DirectionTurn.REVERSE:
            return Point(-1 * direction.row, -1 * direction.col)

        if turn == DirectionTurn.RIGHT:
            sign = 1 if direction.row == 0 else -1
            return Point(direction.col * sign, direction.row * sign)

        if turn == DirectionTurn.LEFT:
            sign = -1 if direction.row == 0 else 1
            return Point(direction.col * sign, direction.row * sign)

        if turn == DirectionTurn.REVERSE_TURN:
            return Point(-1 * direction.col, -1 * direction.row)

        if turn == DirectionTurn.KEEP:
            return direction

        raise Exception(f'Unsupported direction turn "{turn}"')

# TODO: Remove hard-coded border line matches for part 2 and change it to the generic solution
BORDER_3D_LINES: List[Tuple[Line, Line, str]] = [
    (
        Line(Point(99, 0), Point(99, 49)),
        Line(Point(50, 49), Point(99, 49)),
        DirectionTurn.REVERSE_TURN,
    ),
    (
        Line(Point(49, 49), Point(0, 49)),
        Line(Point(100, -1), Point(149, -1)),
        DirectionTurn.REVERSE,
    ),
    (
        Line(Point(-1, 50), Point(-1, 99)),
        Line(Point(150, -1), Point(199, -1)),
        DirectionTurn.REVERSE_TURN,
    ),
    (
        Line(Point(-1, 100), Point(-1, 149)),
        Line(Point(200, 0), Point(200, 49)),
        DirectionTurn.KEEP,
    ),
    (
        Line(Point(0, 150), Point(49, 150)),
        Line(Point(149, 100), Point(100, 100)),
        DirectionTurn.REVERSE,
    ),
    (
        Line(Point(50, 100), Point(50, 149)),
        Line(Point(50, 100), Point(99, 100)),
        DirectionTurn.REVERSE_TURN,
    ),
    (
        Line(Point(150, 50), Point(150, 99)),
        Line(Point(150, 50), Point(199, 50)),
        DirectionTurn.REVERSE_TURN,
    ),
]

class Map:
    def __init__(self, lines: List[str]):
        self.col_walls_by_row = defaultdict(set)
        self.row_walls_by_col = defaultdict(set)
        self.col_range_by_row = {}
        self.row_range_by_col = {}

        # TODO: Add generic function for the creation of the border line matches
        self.border_line_matches = BORDER_3D_LINES
        self._init_from_lines(lines)

    def get_start_point(self) -> Optional[Point]:
        for row in sorted(self.col_range_by_row.keys()):
            col_range = self.col_range_by_row[row]
            for col in range(col_range.start, col_range.end + 1):
                if col not in self.col_walls_by_row[row]:
                    return Point(row, col)
        return None

    def get_valid_2d_point_direction(self, point: Point, direction: Point) -> Tuple[Point, Point]:
        if direction.row == 0:
            col_range = self.col_range_by_row[point.row]
            if point.col < col_range.start:
                point = Point(point.row, col_range.end)
            if point.col > col_range.end:
                point = Point(point.row, col_range.start)
        else:
            row_range = self.row_range_by_col[point.col]
            if point.row < row_range.start:
                point = Point(row_range.end, point.col)
            if point.row > row_range.end:
                point = Point(row_range.start, point.col)

        return point, direction

    def get_valid_3d_point_direction(self, point: Point, direction: Point) -> Tuple[Point, Point]:
        if direction.row == 0:
            col_range = self.col_range_by_row[point.row]
            if point.col < col_range.start or point.col > col_range.end:
                new_point_direction = get_new_3d_point_direction(self.border_line_matches, point, direction)
                if new_point_direction is not None:
                    return new_point_direction
        else:
            row_range = self.row_range_by_col[point.col]
            if point.row < row_range.start or point.row > row_range.end:
                new_point_direction = get_new_3d_point_direction(self.border_line_matches, point, direction)
                if new_point_direction is not None:
                    return new_point_direction

        return point, direction

    def _init_from_lines(self, lines: List[str]):
        rows = len(lines)
        cols = max(len(line) for line in lines)

        for row, line in enumerate(lines):
            min_col = cols
            max_col = 0

            for col, char in enumerate(line):
                if not char.strip():
                    continue

                min_col = min(min_col, col)
                max_col = max(max_col, col)

                if char == '#':
                    self.row_walls_by_col[col].add(row)
                    self.col_walls_by_row[row].add(col)

                if col not in self.row_range_by_col:
                    self.row_range_by_col[col] = Range(rows, 0)

                self.row_range_by_col[col] = Range(
                    min(self.row_range_by_col[col].start, row),
                    max(self.row_range_by_col[col].end, row),
                )

            self.col_range_by_row[row] = Range(min_col, max_col)

def is_point_in_line(line: Line, point: Point) -> bool:
    row, col = point
    min_row = min(line.start.row, line.end.row)
    max_row = max(line.start.row, line.end.row)
    min_col = min(line.start.col, line.end.col)
    max_col = max(line.start.col, line.end.col)

    return min_row <= row <= max_row and min_col <= col <= max_col

def get_new_3d_point_direction(
    border_line_matches: List[Tuple[Line, Line, str]],
    point: Point,
    direction: Point,
) -> Optional[Tuple[Point, Point]]:
    for line1, line2, dir_turn in border_line_matches:
        in_line1 = is_point_in_line(line1, point)
        in_line2 = is_point_in_line(line2, point)

        if not in_line1 and not in_line2:
            continue

        line, new_line = (line1, line2) if in_line1 else (line2, line1)
        drow = line.end.row - point.row
        dcol = line.end.col - point.col

        new_point = point
        new_direction = DirectionTurn.get_new_direction(direction, dir_turn)

        if line.start.row > line.end.row or line.start.col > line.end.col:
            drow = -1 * drow
            dcol = -1 * dcol

        if new_line.start.row > new_line.end.row or new_line.start.col > new_line.end.col:
            drow = -1 * drow
            dcol = -1 * dcol

        if dir_turn == DirectionTurn.REVERSE_TURN:
            new_point = Point(new_line.end.row - dcol, new_line.end.col - drow)

        if dir_turn == DirectionTurn.KEEP:
            new_point = Point(new_line.end.row - drow, new_line.end.col - dcol)

        if dir_turn == DirectionTurn.REVERSE:
            new_point = Point(new_line.end.row - drow, new_line.end.col - dcol)

        new_point = Point(new_point.row + new_direction.row, new_point.col + new_direction.col)
        return new_point, new_direction

    return None

def get_end_point_direction(
    map: Map,
    moves: Union[int, str],
    start_point: Point,
    start_direction: Point,
    get_valid_point_direction: Callable[[Point, Point], Tuple[Point, Point]],
) -> Tuple[Point, Point]:
    point = start_point
    direction = start_direction

    for move in moves:
        if not isinstance(move, int):
            direction = DirectionTurn.get_new_direction(direction, move)
            continue

        for _ in range(move):
            new_point = Point(point.row + direction.row, point.col + direction.col)
            new_direction = direction

            new_point, new_direction = get_valid_point_direction(new_point, new_direction)
            if new_point.col in map.col_walls_by_row[new_point.row]:
                break

            point = new_point
            direction = new_direction

    return point, direction

def get_point_score(point: Point, direction: Point) -> int:
    direction_score = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
    return 1000 * (point.row + 1) + 4 * (point.col + 1) + direction_score.index(direction)

def parse_input_moves(line: str):
    number = 0
    for char in line:
        if char.isdigit():
            number = number * 10 + int(char)
            continue
        yield number
        yield DirectionTurn.RIGHT if char == 'R' else DirectionTurn.LEFT
        number = 0
    if number:
        yield number

def parse_input(lines):
    split_line_i = next(i for i, line in enumerate(lines) if not line.strip())
    map = Map(lines[:split_line_i])
    moves = list(parse_input_moves(lines[split_line_i + 1]))
    return map, moves

def get_first(lines):
    map, moves = parse_input(lines)
    start_point = map.get_start_point()

    end_point, end_direction = get_end_point_direction(
        map,
        moves,
        start_point=start_point,
        start_direction=Point(0, 1),
        get_valid_point_direction=map.get_valid_2d_point_direction,
    )
    return get_point_score(end_point, end_direction)

def get_second(lines):
    map, moves = parse_input(lines)
    start_point = map.get_start_point()

    end_point, end_direction = get_end_point_direction(
        map,
        moves,
        start_point=start_point,
        start_direction=Point(0, 1),
        get_valid_point_direction=map.get_valid_3d_point_direction,
    )
    return get_point_score(end_point, end_direction)

if __name__ == '__main__':
    run(get_first, get_second)
