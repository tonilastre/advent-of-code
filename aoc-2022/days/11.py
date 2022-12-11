import re
from math import floor
from functools import reduce
from collections import namedtuple
from typing import Iterable, Callable, TypeVar, List, Iterator, Optional
from aoc import run, get_int_numbers

T = TypeVar('T')
OpType = Callable[[int], int]

OPERATION_BY_SIGN = {
    '*': lambda *v: reduce(lambda a, b: a * b, v),
    '+': lambda *v: sum(v),
}

MonkeyInspectResult = namedtuple('MonkeyInspectResult', 'monkey_index, item')

class Monkey:
    def __init__(self, index: int, items: List[int], inspect_op: OpType, test_op: OpType):
        self.index = index
        self.items = items
        self.item_inspect_count = 0
        self.inspect_op = inspect_op
        self.test_op = test_op

    def iter_inspections(self, custom_op: Optional[OpType] = None) -> Iterator[MonkeyInspectResult]:
        while self.items:
            self.item_inspect_count += 1
            raw_item = self.items.pop(0)
            op_item = self.inspect_op(raw_item)
            new_item = custom_op(op_item) if custom_op else op_item
            new_monkey_index = self.test_op(new_item)
            yield MonkeyInspectResult(new_monkey_index, new_item)

    def __hash__(self):
        return self.index

def batch_lines(lines: Iterable[T], batch_by: Callable[[T], bool]) -> Iterator[List[T]]:
    batch: List[T] = []
    for line in lines:
        if not batch_by(line):
            batch.append(line)
            continue
        if batch:
            yield batch
            batch = []

    if batch:
        yield batch

def parse_input_inspect_operation(line: str) -> OpType:
    match = re.search(r'= (old|\d+) (.) (old|\d+)', line)
    if not match:
        raise Exception(f'Unsupported operation: {line}')

    value1, operator, value2 = match.groups()
    if operator not in OPERATION_BY_SIGN:
        raise Exception(f'Unsupported operation sign: {operator}')

    op = OPERATION_BY_SIGN[operator]
    values = [value1, value2]
    op_values = [(lambda v: v) if value == 'old' else (lambda _: int(value)) for value in values]

    return lambda v: op(*(op_value(v) for op_value in op_values))

def parse_input_test_operation(lines: List[str]) -> OpType:
    if 'divisible' not in lines[0]:
        raise Exception(f'Unsupported test operation: {lines[0]}')

    div_number = get_int_numbers(lines[0])[0]
    return_by_div = {}

    for line in lines[1:]:
        match = re.search(r'If (.*?):.*(\d+)$', line)
        if not match:
            raise Exception(f'Unsupported test result: {line}')

        div_result, return_result = match.groups()
        return_by_div[div_result] = int(return_result)

    return lambda v: return_by_div[str(v % div_number == 0).lower()]

def parse_input_monkey(lines) -> Monkey:
    index = -1
    items = []
    inspect_op = None
    test_op = None

    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('Monkey '):
            index = get_int_numbers(line)[0]
            continue

        if line.startswith('Starting items:'):
            items = get_int_numbers(line)
            continue

        if line.startswith('Operation:'):
            inspect_op = parse_input_inspect_operation(line)
            continue

        if line.startswith('Test:'):
            test_op = parse_input_test_operation(lines[i:i + 3])
            continue

    return Monkey(index, items, inspect_op, test_op)

def parse_input_monkeys(lines) -> Iterator[Monkey]:
    for line_batch in batch_lines(lines, batch_by=lambda line: not line.strip()):
        yield parse_input_monkey(line_batch)

def simulate_inspections(monkeys: List[Monkey], rounds: int, custom_op: Optional[OpType] = None):
    monkey_by_index = {m.index: m for m in monkeys}
    for _ in range(rounds):
        for monkey in monkeys:
            for inspection in monkey.iter_inspections(custom_op=custom_op):
                monkey_by_index[inspection.monkey_index].items.append(inspection.item)
    return monkeys

def get_first(lines):
    monkeys = list(parse_input_monkeys(lines))
    monkeys = simulate_inspections(monkeys, rounds=20, custom_op=lambda v: floor(v / 3))
    inspect_counts = sorted((m.item_inspect_count for m in monkeys), reverse=True)
    return inspect_counts[0] * inspect_counts[1]

def get_second(lines):
    monkeys = list(parse_input_monkeys(lines))
    divs = [get_int_numbers(line)[0] for line in lines if 'Test: divisible' in line]
    div_mod = reduce(lambda a, b: a * b, divs)

    monkeys = simulate_inspections(monkeys, rounds=10000, custom_op=lambda v: v % div_mod)
    inspect_counts = sorted((m.item_inspect_count for m in monkeys), reverse=True)
    return inspect_counts[0] * inspect_counts[1]

if __name__ == '__main__':
    run(get_first, get_second)
