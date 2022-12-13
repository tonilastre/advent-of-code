from aoc import run
from math import prod
from functools import cmp_to_key
from typing import Optional

def parse_line(line):
    clean_line = line.replace('[', ' [ ').replace(']', ' ] ').replace(',', ' ').strip()
    chars = filter(bool, clean_line.split(' '))
    stack = [list()]

    for char in chars:
        if char.isdigit():
            stack[-1].append(int(char))
            continue

        if char == '[':
            stack.append(list())
            continue

        if char == ']':
            last_item = stack.pop()
            stack[-1].append(last_item)
            continue

    return stack[-1].pop()

def parse_lines_to_pairs(lines):
    for i in range(0, len(lines), 3):
        yield parse_line(lines[i]), parse_line(lines[i + 1])

def is_int(value):
    return isinstance(value, int)

def is_list(value):
    return isinstance(value, list)

def is_right_order(left, right) -> Optional[bool]:
    if is_int(left) and is_int(right):
        return None if left == right else left < right

    if is_list(left) and is_list(right):
        for l, r in zip(left, right):
            is_right = is_right_order(l, r)
            if is_right is not None:
                return is_right
        return is_right_order(len(left), len(right))

    if is_int(left) and is_list(right):
        return is_right_order([left], right)

    if is_list(left) and is_int(right):
        return is_right_order(left, [right])

    return False

def is_right_order_compare(left, right) -> int:
    is_right = is_right_order(left, right)
    if is_right is None:
        return 0
    return -1 if is_right else 1

def get_first(lines):
    pairs = list(parse_lines_to_pairs(lines))
    right_sum = 0

    for i, (left, right) in enumerate(pairs, start=1):
        if is_right_order(left, right):
            right_sum += i

    return right_sum

def get_second(lines):
    packages = ([[2]], [[6]])

    items = [parse_line(line) for line in lines if line]
    items.extend(packages)
    items.sort(key=cmp_to_key(is_right_order_compare))

    package_indexes = [i for i, item in enumerate(items, start=1) if item in packages]
    return prod(package_indexes)

if __name__ == '__main__':
    run(get_first, get_second)
