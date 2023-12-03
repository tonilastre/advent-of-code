import re
from aoc import run
from typing import Iterator
from collections import namedtuple

Position = namedtuple('Position', 'x, y')
Sign = namedtuple('Sign', 'value, position')
Number = namedtuple('Number', 'value, start, end')

def is_adjacent(number: Number, sign: Sign) -> bool:
    x, y = sign.position
    start_x, start_y = number.start
    end_x, end_y = number.end
    return start_x - 1 <= x <= end_x + 1 and start_y - 1 <= y <= end_y + 1

def parse_signs(lines) -> Iterator[Sign]:
    for i, line in enumerate(lines):
        for match in re.finditer('[^\d.]', line):
            yield Sign(match.group(), Position(i, match.start()))

def parse_numbers(lines) -> Iterator[Number]:
    for i, line in enumerate(lines):
        for match in re.finditer('\d+', line):
            number = match.group()
            x, y = i, match.start()
            yield Number(int(number), Position(x, y), Position(x, y + len(number) - 1))

def get_first(lines):
    signs = list(parse_signs(lines))
    return sum(
        number.value
        for number in parse_numbers(lines)
        if any(is_adjacent(number, s) for s in signs)
    )

def get_second(lines):
    numbers = list(parse_numbers(lines))
    signs = (sign for sign in parse_signs(lines) if sign.value == '*')

    result = 0
    for sign in signs:
        adj_numbers = [number for number in numbers if is_adjacent(number, sign)]
        if len(adj_numbers) == 2:
            result += adj_numbers[0].value * adj_numbers[1].value
    return result

if __name__ == '__main__':
    run(get_first, get_second)
