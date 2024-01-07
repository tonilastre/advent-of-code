import re
from typing import Tuple, List
from functools import cache
from aoc import run, get_int_numbers

def parse_line(line: str) -> Tuple[str, List[int]]:
    value, numbers = line.split(' ', maxsplit=1)
    return value, get_int_numbers(numbers)

def get_segments(chars: str) -> List[str]:
    return re.findall(r'([^\.]+)', ''.join(chars))

@cache
def solve_cached(chars: str, numbers: Tuple[int]) -> int:
    segments = get_segments(chars)
    if '?' not in chars:
        if len(segments) != len(numbers):
            return 0
        return int(all(len(s) == n for s, n in zip(segments, numbers)))

    if len(segments) <= 1:
        chars1 = chars.replace('?', '.', 1)
        chars2 = chars.replace('?', '#', 1)
        r1 = solve(chars1, numbers)
        r2 = solve(chars2, numbers)
        return r1 + r2

    main_chars = segments[0]
    next_chars = '.'.join(segments[1:])

    result = 0
    for i in range(0, len(numbers) + 1):
        main_numbers = numbers[:i]
        min_len = sum(main_numbers) + max(len(main_numbers) - 1, 0)
        if min_len > len(main_chars):
            break

        r1 = solve(main_chars, main_numbers)
        if r1 == 0:
            continue

        r2 = solve(next_chars, numbers[i:])
        result += r1 * r2
    return result

def solve(chars, numbers):
    return solve_cached(chars.strip('.'), numbers)

def get_first(lines):
    sol = 0
    for line in lines:
        chars, numbers = parse_line(line)
        sol += solve(chars, tuple(numbers))
    return sol

def get_second(lines):
    sol = 0
    size = 5
    for line in lines:
        chars, numbers = parse_line(line)
        new_chars = '?'.join([chars] * size)
        new_numbers = numbers * size
        sol += solve(new_chars, tuple(new_numbers))
    return sol

if __name__ == '__main__':
    run(get_first, get_second)
