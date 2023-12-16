from aoc import run
from collections import namedtuple, defaultdict

Lens = namedtuple('Lens', 'label, value')

def get_hash(line: str):
    value = 0
    for char in line:
        value = ((value + ord(char)) * 17) % 256
    return value

def parse_input(line: str):
    if '-' in line:
        return '-', Lens(line[:-1], 0)
    parts = line.split('=', maxsplit=1)
    return '=', Lens(parts[0], int(parts[1]))

def get_first(lines):
    result = 0
    for part in lines[0].split(','):
        result += get_hash(part)
    return result

def get_second(lines):
    boxes = defaultdict(list)
    for part in lines[0].split(','):
        sign, lens = parse_input(part)
        box = get_hash(lens.label)
        lenses = boxes.get(box, [])
        index = next((i for i, l in enumerate(lenses) if l.label == lens.label), -1)
        if sign == '-' and index >= 0:
            del boxes[box][index]
        if sign == '=':
            if index == -1:
                boxes[box].append(lens)
            else:
                boxes[box][index] = lens

    power = 0
    for box, lenses in boxes.items():
        if not lenses:
            continue
        for i, lens in enumerate(lenses):
            power += (box + 1) * (i + 1) * lens.value
    return power

if __name__ == '__main__':
    run(get_first, get_second)
