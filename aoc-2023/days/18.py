from aoc import run, pairwise
from typing import List
from collections import namedtuple

Position = namedtuple('Position', 'x, y')
Move = namedtuple('Move', 'direction, count')

DIFF_BY_DIRECTION = {
    'R': lambda i: Position(0, i),
    'D': lambda i: Position(i, 0),
    'L': lambda i: Position(0, -i),
    'U': lambda i: Position(-i, 0),
}

def get_area(positions: List[Position]):
    area = 0
    lens = 0
    for pos1, pos2 in pairwise(positions):
        area += (pos1.x * pos2.y - pos2.x * pos1.y)
        lens += abs((pos1.x - pos2.x) + (pos1.y - pos2.y))
    return (abs(area) + lens) / 2 + 1

def parse_line_simple(line: str):
    direction, count, _ = line.split(' ', maxsplit=2)
    return Move(direction, int(count))

def parse_line_complex(line: str):
    parts = line.split(' ', maxsplit=2)
    color = parts[2][1:-1]
    direction = ['R', 'D', 'L', 'U'][int(color[-1])]
    count = int(f'0x{color[1:-1]}', 16)
    return Move(direction, count)

def get_positions(moves: List[Move], start_position=Position(0, 0)):
    position = start_position
    positions: List[Position] = [start_position]

    for move in moves:
        dx, dy = DIFF_BY_DIRECTION[move.direction](move.count)
        position = Position(position.x + dx, position.y + dy)
        positions.append(position)

    return positions

def get_first(lines):
    moves = [parse_line_simple(line) for line in lines]
    positions = get_positions(moves)
    return int(get_area(positions))

def get_second(lines):
    moves = [parse_line_complex(line) for line in lines]
    positions = get_positions(moves)
    return int(get_area(positions))

if __name__ == '__main__':
    run(get_first, get_second)
