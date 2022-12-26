from math import log
from aoc import run

class SnafuNum:
    CHARS = ('=', '-', '0', '1', '2')

    def __init__(self, value: str):
        self.value = value

    def __int__(self) -> int:
        return self.as_int()

    def __str__(self):
        return self.value

    def as_int(self) -> int:
        number = 0
        zero_index = SnafuNum.CHARS.index('0')

        for i, char in enumerate(reversed(self.value)):
            digit = len(SnafuNum.CHARS) ** i
            index = SnafuNum.CHARS.index(char) - zero_index
            number += digit * index
        return number

    @staticmethod
    def from_int(number: int) -> 'SnafuNum':
        if number == 0:
            return '0'

        size = len(SnafuNum.CHARS)
        # Zero is 000, which is on index 2 in list of CHARS
        zero_index = SnafuNum.CHARS.index('0')
        indexes = []

        carry_over = 0
        while number:
            remainder = number % size + zero_index + carry_over
            number = number // size

            carry_over = remainder // size
            remainder = remainder % size
            indexes.append(remainder)

        if carry_over:
            indexes.append(carry_over + zero_index)

        value = ''.join(reversed([SnafuNum.CHARS[i] for i in indexes]))
        return SnafuNum(value)

def get_first(lines):
    numbers = [SnafuNum(line) for line in lines]
    numbers_sum = sum(int(n) for n in numbers)
    return SnafuNum.from_int(numbers_sum)

if __name__ == '__main__':
    run(get_first)
