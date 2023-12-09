import re
from aoc import run
from typing import List
from itertools import cycle

def gcd(num1, num2):
    if num1 < num2:
        num1, num2 = num2, num1
    if num2 == 0:
        return num1
    return gcd(num2, num1 % num2)

def lcm(*numbers):
    if len(numbers) == 0:
        return 0
    result = numbers[0]
    for num in numbers[1:]:
        result = num // gcd(num, result) * result
    return result

def parse_line(line: str):
    return re.findall('\w+', line)

def parse_nodes(lines: List[str]):
    nodes_by_name = dict()
    for line in lines:
        names = parse_line(line)
        if len(names) != 3:
            continue
        name, left, right = names
        nodes_by_name[name] = (left, right)
    return nodes_by_name

def get_first(lines):
    moves = cycle(lines[0].strip())
    nodes_by_name = parse_nodes(lines[1:])
    name = 'AAA'
    step = 0
    while name != 'ZZZ':
        step += 1
        move = next(moves)
        left, right = nodes_by_name[name]
        name = left if move == 'L' else right
    return step

def get_second(lines):
    moves = lines[0].strip()
    nodes_by_name = parse_nodes(lines[1:])

    names = [name for name in nodes_by_name.keys() if name.endswith('A')]
    step_checkpoints = []
    min_repeats = 3

    for name in names:
        step_diffs = []
        step = 0
        prev_step = 0
        current_name = name

        while True:
            unique_step_diffs = set(step_diffs) if len(step_diffs) >= min_repeats else set()
            if step > len(moves) and len(unique_step_diffs) == 1:
                step_checkpoints.append(unique_step_diffs.pop())
                break
            move = moves[step % len(moves)]
            step += 1
            left, right = nodes_by_name[current_name]
            current_name = left if move == 'L' else right
            if not current_name.endswith('Z'):
                continue

            diff = step - prev_step
            prev_step = step
            step_diffs.append(diff)

    return lcm(*step_checkpoints)

if __name__ == '__main__':
    run(get_first, get_second)
