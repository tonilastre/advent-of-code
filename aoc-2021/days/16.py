from aoc import run
from collections import namedtuple
from functools import reduce

Statement = namedtuple('Statement', 'version, type, items')

statement_type_functions = {
    0: lambda s: sum(map(run_parsed_statement, s.items)),
    1: lambda s: reduce(lambda a, b: a * b, map(run_parsed_statement, s.items)),
    2: lambda s: min(map(run_parsed_statement, s.items)),
    3: lambda s: max(map(run_parsed_statement, s.items)),
    4: lambda s: s.items[0],
    5: lambda s: int(run_parsed_statement(s.items[0]) > run_parsed_statement(s.items[1])),
    6: lambda s: int(run_parsed_statement(s.items[0]) < run_parsed_statement(s.items[1])),
    7: lambda s: int(run_parsed_statement(s.items[0]) == run_parsed_statement(s.items[1]))
}

def take(arr, n = 1):
    return [arr.pop(0) for _ in range(n) if arr]

def to_decimal(binary):
    return int("".join(binary), 2) if binary else 0

def hex_to_binary(hex_code, n = 4):
    binary = []
    for hex_digit in hex_code:
        # Binary string format: 0bXXXX
        binary_str = bin(int(hex_digit, 16))[2:]
        # Prefix with zeroes
        binary.extend(list(binary_str.zfill(n)))
    return binary

def parse_literal_number(binary):
    binary_number = []
    while len(binary):
        binary_segment = take(binary, 5)
        binary_number.extend(binary_segment[1:])
        # Indicates last group
        if binary_segment[0] == '0':
            break
    return to_decimal(binary_number)

def parse_operator(binary):
    package_type = to_decimal(take(binary))

    if package_type:
        packages_count = to_decimal(take(binary, 11))
        for _ in range(packages_count):
            yield parse_statement(binary)
    else:
        packages_size = to_decimal(take(binary, 15))
        sub_binary = take(binary, packages_size)
        while len(sub_binary):
            yield parse_statement(sub_binary)

def parse_statement(binary):
    version = to_decimal(take(binary, 3))
    type = to_decimal(take(binary, 3))
    items = []

    if type == 4:
        items.append(parse_literal_number(binary))
    else:
        for c in parse_operator(binary):
            items.append(c)

    return Statement(version, type, items)

def iter_versions(statement):
    if not isinstance(statement, Statement):
        return

    yield statement.version
    for item in statement.items:
        yield from iter_versions(item)

def run_parsed_statement(p):
    return statement_type_functions[p.type](p)

def get_first(lines):
    for line in lines:
        binary = hex_to_binary(line)
        statement = parse_statement(binary)
        versions_sum = sum(iter_versions(statement))
        # print(f'{str(versions_sum)}\t{line}')
    return versions_sum

def get_second(lines):
    for line in lines:
        binary = hex_to_binary(line)
        statement = parse_statement(binary)
        result = run_parsed_statement(statement)
        # print(f'{str(result)}\t{line}')
    return result

if __name__ == '__main__':
    run(get_first, get_second)
