import re
from aoc import run
from typing import Tuple

NUM_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
NUM_REGEX = r'([1-9])'
NUM_WORDS_REGEX = f'([1-9]|{"|".join(NUM_WORDS)})'

def translate_digit(digit: str) -> str:
    return digit if digit.isdigit() else str(NUM_WORDS.index(digit) + 1)

def get_border_digits(line: str, parse_words = False) -> Tuple[int, int]:
    regex = NUM_WORDS_REGEX if parse_words else NUM_REGEX

    first_digit = re.search(f'^.*?{regex}', line).group(1)
    last_digit = re.search(f'.*{regex}.*?$', line).group(1)

    digits = [first_digit, last_digit]
    return tuple(int(translate_digit(d)) for d in digits)

def get_first(lines):
    digits = (get_border_digits(line) for line in lines)
    return sum((d[0] * 10 + d[1]) for d in digits)

def get_second(lines):
    digits = (get_border_digits(line, parse_words=True) for line in lines)
    return sum((d[0] * 10 + d[1]) for d in digits)

if __name__ == '__main__':
    run(get_first, get_second)
