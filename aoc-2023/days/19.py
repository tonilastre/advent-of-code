import re
from typing import Optional, List, Dict
from aoc import run
from operator import mul
from functools import reduce
from collections import namedtuple

APPROVE = 'A'
REJECT = 'R'
VARS = 'xmas'
Range = namedtuple('Range', 'start, end')

class Node:
    def __init__(self, name: str):
        self.name = name
        self.true_child: Optional[Node] = None
        self.false_child: Optional[Node] = None

    def add_true_child(self, node: 'Node'):
        self.true_child = node

    def add_false_child(self, node: 'Node'):
        self.false_child = node

    def is_approved(self):
        return self.name == APPROVE

    def is_rejected(self):
        return self.name == REJECT

    def evaluate(self, values: List[int]):
        return self.true_child if self.true_child else self.false_child

    def __eq__(self, other):
        return isinstance(other, Node) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

class NameNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def add_true_child(self, node: 'Node'):
        self.true_child = node
        self.false_child = node

    def add_false_child(self, node: 'Node'):
        self.true_child = node
        self.false_child = node

class CheckLtNode(Node):
    def __init__(self, name: str, index: int, value: int):
        super().__init__(name)
        self.index = index
        self.value = value

    def evaluate(self, values: List[int]):
        return self.true_child if values[self.index] < self.value else self.false_child

class CheckGtNode(Node):
    def __init__(self, name: str, index: int, value: int):
        super().__init__(name)
        self.index = index
        self.value = value

    def evaluate(self, values: List[int]):
        return self.true_child if values[self.index] > self.value else self.false_child

def parse_workflows(lines: List[str]):
    node_by_name: Dict[str, Node] = {
        APPROVE: Node(APPROVE),
        REJECT: Node(REJECT),
    }
    for line in lines:
        name, _ = line.split('{', maxsplit=1)
        node_by_name[name] = Node(name)

    intermediate_node_index = 1
    for line in lines:
        name, rules = line[:-1].split('{', maxsplit=1)
        node = node_by_name[name]
        for rule in rules.split(','):
            m = re.match(r'^(\w)(<|>)(\d+):(\w+)$', rule)
            if not m:
                next_node = node_by_name[rule]
                node.add_false_child(next_node)
                break

            var, check, number, true_node_name = m.groups()
            index = VARS.index(var)

            new_node_name = str(intermediate_node_index)
            intermediate_node_index += 1
            if check == '<':
                new_node = CheckLtNode(new_node_name, index, int(number))
            else:
                new_node = CheckGtNode(new_node_name, index, int(number))

            node.add_false_child(new_node)
            new_node.add_true_child(node_by_name[true_node_name])
            node = new_node

    return node_by_name

def parse_data_line(line: str) -> List[int]:
    values = [0] * len(VARS)
    for part in re.findall(r'\w=\d+', line):
        var, number = part.split('=', maxsplit=1)
        values[VARS.index(var)] = int(number)
    return values

def parse_input(lines):
    split_line_index = lines.index('')
    nodes_by_name = parse_workflows(lines[:split_line_index])
    values = [parse_data_line(line) for line in lines[split_line_index + 1:]]
    return nodes_by_name, values

def intersects_with_range(range1: Range, range2: Range) -> bool:
    return range1.end > range2.start and range1.start < range2.end

def intersect_ranges(ranges: List[Range]) -> List[Range]:
    if not ranges:
        return []
    final_ranges: List[Range] = [ranges[0]]
    for range in ranges[1:]:
        final_ranges = [
            Range(max(r.start, range.start), min(r.end, range.end))
            for r in final_ranges
            if intersects_with_range(r, range)
        ]
    return final_ranges

def reduce_ranges(ranges: List[Range]) -> int:
    return sum(range.end - range.start for range in ranges)

def get_combinations_count(node: Node, ranges: List[List[Range]], min_value: int, max_value: int):
    if node.is_approved():
        final_ranges = (reduce_ranges(intersect_ranges(r)) for r in ranges)
        return reduce(mul, final_ranges)
    if node.is_rejected():
        return 0

    if isinstance(node, CheckGtNode):
        true_ranges = [r.copy() for r in ranges]
        true_ranges[node.index].append(Range(node.value + 1, max_value))
        true_count = get_combinations_count(node.true_child, true_ranges, min_value, max_value)

        false_ranges = [r.copy() for r in ranges]
        false_ranges[node.index].append(Range(min_value, node.value + 1))
        false_count = get_combinations_count(node.false_child, false_ranges, min_value, max_value)

        return true_count + false_count

    if isinstance(node, CheckLtNode):
        true_ranges = [r.copy() for r in ranges]
        true_ranges[node.index].append(Range(min_value, node.value))
        true_count = get_combinations_count(node.true_child, true_ranges, min_value, max_value)

        false_ranges = [r.copy() for r in ranges]
        false_ranges[node.index].append(Range(node.value, max_value))
        false_count = get_combinations_count(node.false_child, false_ranges, min_value, max_value)

        return true_count + false_count

    return get_combinations_count(node.true_child or node.false_child, ranges, min_value, max_value)

def get_first(lines):
    nodes_by_name, values = parse_input(lines)

    result = 0
    for value in values:
        node = nodes_by_name['in']
        while not node.is_approved() and not node.is_rejected():
            node = node.evaluate(value)
        if node.is_approved():
            result += sum(value)
    return result

def get_second(lines):
    nodes_by_name, _ = parse_input(lines)
    MIN, MAX = 1, 4001
    ranges = [[Range(MIN, MAX)]] * len(VARS)

    return get_combinations_count(nodes_by_name['in'], ranges, MIN, MAX)

if __name__ == '__main__':
    run(get_first, get_second)
