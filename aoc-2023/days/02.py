import re
from aoc import run
from typing import Any, List
from dataclasses import dataclass

@dataclass
class Reveal:
    red: int
    green: int
    blue: int

    def get_power(self) -> int:
        return self.red * self.green * self.blue

    def __le__(self, obj: Any):
        if not isinstance(obj, Reveal):
            return False
        return self.red <= obj.red and self.green <= obj.green and self.blue <= obj.blue

    @staticmethod
    def max(*reveals):
        max_reveal = Reveal(red=0, green=0, blue=0)
        for reveal in reveals:
            max_reveal.red = max(max_reveal.red, reveal.red)
            max_reveal.green = max(max_reveal.green, reveal.green)
            max_reveal.blue = max(max_reveal.blue, reveal.blue)
        return max_reveal

def parse_reveal(line: str) -> Reveal:
    count_by_color = { 'red': 0, 'green': 0, 'blue': 0 }
    for match in re.finditer('(\d+) (red|green|blue)', line):
        number, color = match.groups()
        count_by_color[color] = int(number)
    return Reveal(**count_by_color)

def parse_line(line: str) -> List[Reveal]:
    parts = line.split(';')
    return [parse_reveal(part) for part in parts]

def get_first(lines):
    check = Reveal(red=12, green=13, blue=14)
    games = [parse_line(line) for line in lines]
    result = 0
    for index, game in enumerate(games, start=1):
        if all(g <= check for g in game):
            result += index
    return result

def get_second(lines):
    games = [parse_line(line) for line in lines]
    max_reveals = [Reveal.max(*g) for g in games]
    powers = [r.get_power() for r in max_reveals]
    return sum(powers)

if __name__ == '__main__':
    run(get_first, get_second)
