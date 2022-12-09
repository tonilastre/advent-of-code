from aoc import run
from math import ceil
from collections import namedtuple

Position = namedtuple('Position', 'x, y')

moves_by_direction = {
    'U': lambda dy: ((0, 1) for _ in range(dy)),
    'R': lambda dx: ((1, 0) for _ in range(dx)),
    'D': lambda dy: ((0, -1) for _ in range(dy)),
    'L': lambda dx: ((-1, 0) for _ in range(dx)),
}

def parse_line(line):
    direction, steps = line.split(' ', maxsplit=1)
    return moves_by_direction[direction](int(steps))

def abs_ceil(num):
    return ceil(num) if num >= 0 else -ceil(-num)

def get_new_tail_position(tail: Position, head: Position) -> Position:
    diff_x = head.x - tail.x
    diff_y = head.y - tail.y
    if abs(diff_x) <= 1 and abs(diff_y) <= 1:
        return tail
    return Position(tail.x + abs_ceil(diff_x / 2), tail.y + abs_ceil(diff_y / 2))

def get_unique_tail_positions(start_position, moves, rope_len=2):
    rope = [start_position] * rope_len
    unique_tails = set([start_position])

    for move in moves:
        for dx, dy in move:
            old_head = rope[0]
            old_tail = rope[-1]

            rope[0] = Position(old_head.x + dx, old_head.y + dy)
            for i in range(1, len(rope)):
                rope[i] = get_new_tail_position(rope[i], rope[i - 1])

            new_tail = rope[-1]
            if new_tail != old_tail:
                unique_tails.add(new_tail)

    return unique_tails

def get_first(lines):
    moves = [parse_line(line) for line in lines]
    return len(get_unique_tail_positions(Position(0, 0), moves, rope_len=2))

def get_second(lines):
    moves = [parse_line(line) for line in lines]
    return len(get_unique_tail_positions(Position(0, 0), moves, rope_len=10))

if __name__ == '__main__':
    run(get_first, get_second)
