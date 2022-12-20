from itertools import chain
from typing import List, Iterator
from collections import namedtuple
from aoc import run

Number = namedtuple('Number', 'value, index')

def get_mixed_numbers(numbers: List[Number], n: int = 1) -> List[Number]:
    # Tuple (number, index) is used to make each number unique
    # in order to find it in the mixed list of numbers
    initial_numbers = list(numbers)
    numbers_len = len(numbers)

    for _ in range(n):
        for initial_number in initial_numbers:
            value = initial_number.value
            if value == 0:
                continue

            # numbers_len - 1 because the current item should
            # not be counted (as it moves, e.g. linked-list movement)
            movement = value % (numbers_len - 1)

            start = numbers.index(initial_number)
            end = (start + movement) % numbers_len

            if start == end:
                continue

            if start < end:
                new_numbers = list(chain(
                    numbers[:start],
                    numbers[start + 1:end + 1],
                    [initial_number],
                    numbers[end + 1:],
                ))
            else:
                new_numbers = list(chain(
                    numbers[:end + 1],
                    [initial_number],
                    numbers[end + 1:start],
                    numbers[start + 1:],
                ))
            numbers = new_numbers

    return numbers

def iter_zero_offset_numbers(numbers: List[Number], offsets: List[int]) -> Iterator[Number]:
    zero_index = next((i for i, n in enumerate(numbers) if n.value == 0), -1)
    if zero_index == -1:
        return

    for offset in offsets:
        index = (zero_index + offset) % len(numbers)
        yield numbers[index]

def get_first(lines):
    numbers = [Number(int(line), i) for i, line in enumerate(lines)]
    numbers = get_mixed_numbers(numbers, n=1)
    return sum(n.value for n in iter_zero_offset_numbers(numbers, [1000, 2000, 3000]))

def get_second(lines):
    numbers = [Number(int(line) * 811589153, i) for i, line in enumerate(lines)]
    numbers = get_mixed_numbers(numbers, n=10)
    return sum(n.value for n in iter_zero_offset_numbers(numbers, [1000, 2000, 3000]))

if __name__ == '__main__':
    run(get_first, get_second)
