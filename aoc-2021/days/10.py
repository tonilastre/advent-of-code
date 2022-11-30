from aoc import run
from functools import reduce
from statistics import median
from collections import deque

class AutoComplete:
    PAIRS = ['()', '[]', '{}', '<>']

    def __init__(self, line):
        self.stack = deque()
        self.opened_to_closed = { opened: closed for opened, closed in AutoComplete.PAIRS }
        self.closed_to_opened = { closed: opened for opened, closed in AutoComplete.PAIRS }
        self.corrupted_char = None

        self.__parse(line)

    def is_corrupted(self):
        return self.corrupted_char is not None

    def get_completed_line(self):
        return "".join(reversed(list(self.opened_to_closed[item] for item in self.stack)))

    def __parse(self, line):
        for char in line:
            if char in self.opened_to_closed:
                self.stack.append(char)

            if char in self.closed_to_opened:
                actual_item = self.stack.pop() if self.stack else None
                expected_item = self.closed_to_opened[char]
                if expected_item != actual_item:
                    self.corrupted_char = char
                    break

def get_completed_score(line):
    points = { char: i for i, char in enumerate(')]}>', start=1) }
    return reduce(lambda a, b: a * 5 + b, (points[char] for char in line), 0)

def get_first(lines):
    points = { None: 0, ')': 3, ']': 57, '}': 1197, '>': 25137 }
    return sum(points[AutoComplete(line).corrupted_char] for line in lines)

def get_second(lines):
    completions = (AutoComplete(line) for line in lines)
    scores = (get_completed_score(c.get_completed_line()) for c in completions if not c.is_corrupted())
    return median(s for s in scores if s > 0)

if __name__ == '__main__':
    run(get_first, get_second)
