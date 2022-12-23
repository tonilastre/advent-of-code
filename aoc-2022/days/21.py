from typing import Dict, Tuple, Union, Set
from collections import namedtuple
from aoc import run, get_int_numbers

Operation = namedtuple('Operation', 'op, left, right')

ROOT_VAR = 'root'
HUMN_VAR = 'humn'

CALLABLE_BY_OP = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}

# total = left <op> right
REVERSE_OP_FOR_LEFT = {
    '+': lambda final, right: Operation('-', final, right),
    '-': lambda final, right: Operation('+', final, right),
    '*': lambda final, right: Operation('/', final, right),
    '/': lambda final, right: Operation('*', final, right),
}

# total = left <op> right
REVERSE_OP_FOR_RIGHT = {
    '+': lambda final, left: Operation('-', final, left),
    '-': lambda final, left: Operation('-', left, final),
    '*': lambda final, left: Operation('/', final, left),
    '/': lambda final, left: Operation('/', left, final),
}

def is_number(value: Union[int, Operation]) -> bool:
    return isinstance(value, int)

def parse_input_line(line: str) -> Tuple[str, Union[int, Operation]]:
    name, operation = line.split(':', maxsplit=1)
    numbers = get_int_numbers(operation)
    if numbers:
        return (name, numbers[0])
    left, op, right = operation.strip().split(' ', maxsplit=3)
    return (name, Operation(op, left, right))

def strip_equations(equation_by_name: Dict[str, Union[int, Operation]]) -> Dict[str, Union[int, Operation]]:
    value_by_name = {name: value for name, value in equation_by_name.items() if is_number(value)}
    names_queue = [name for name in equation_by_name.keys() if name not in value_by_name]

    while names_queue:
        updated_names_queue = []
        for name in names_queue:
            if name in value_by_name:
                continue

            op, left, right = equation_by_name.get(name)
            left_value = value_by_name.get(left)
            right_value = value_by_name.get(right)

            if left_value is None or right_value is None:
                updated_names_queue.append(name)
                continue

            value_by_name[name] = CALLABLE_BY_OP[op](left_value, right_value)

        if len(updated_names_queue) == len(names_queue):
            break

        names_queue = updated_names_queue

    unresolved_equations = [(name, equation_by_name[name]) for name in names_queue]
    resolved_equations = [(name, value) for name, value in value_by_name.items()]

    return dict(unresolved_equations + resolved_equations)

def reverse_equations(equation_by_name: Dict[str, Union[int, Operation]], variable_names: Set[str]) -> Dict[str, Union[int, Operation]]:
    reversed_equation_by_name = {name: value for name, value in equation_by_name.items() if is_number(value)}

    for name, value in equation_by_name.items():
        if is_number(reversed_equation_by_name.get(name)):
            continue

        if is_number(value):
            reversed_equation_by_name[name] = value
            continue

        op, left, right = value
        left_value = reversed_equation_by_name.get(left)
        right_value = reversed_equation_by_name.get(right)

        if right in variable_names or is_number(left_value):
            reversed_equation_by_name[right] = REVERSE_OP_FOR_RIGHT[op](name, left)
            continue

        if left in variable_names or is_number(right_value):
            reversed_equation_by_name[left] = REVERSE_OP_FOR_LEFT[op](name, right)
            continue

        if right_value is None:
            reversed_equation_by_name[right] = REVERSE_OP_FOR_RIGHT[op](name, left)
        if left_value is None:
            reversed_equation_by_name[left] = REVERSE_OP_FOR_LEFT[op](name, right)

    return reversed_equation_by_name

def get_first(lines):
    equation_by_name = dict([parse_input_line(line) for line in lines])
    equation_by_name = strip_equations(equation_by_name)
    return equation_by_name.get(ROOT_VAR)

def get_second(lines):
    equation_by_name = dict([parse_input_line(line) for line in lines])
    _, root_left, root_right = equation_by_name[ROOT_VAR]

    del equation_by_name[ROOT_VAR]
    del equation_by_name[HUMN_VAR]
    equation_by_name = strip_equations(equation_by_name)

    left_value = equation_by_name[root_left]
    right_value = equation_by_name[root_right]
    value = left_value if is_number(left_value) else right_value
    if not is_number(value):
        raise Exception('Unable to get a single number from left or right equations')

    reversed_equation_by_name = reverse_equations(equation_by_name, {HUMN_VAR})
    reversed_equation_by_name[root_left] = value
    reversed_equation_by_name[root_right] = value

    reversed_equation_by_name = strip_equations(reversed_equation_by_name)
    return reversed_equation_by_name.get(HUMN_VAR)

if __name__ == '__main__':
    run(get_first, get_second)
