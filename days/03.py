from aoc import run

def to_decimal(binary):
    return int("".join(binary), 2)

def reverse_binary(binary):
    return ["1" if b == "0" else "0" for b in binary]

def get_first(lines):
    most_common_bits = []

    for i in range(0, len(lines[0])):
        ones = sum(line[i] == "1" for line in lines)
        most_common_bits.append("1" if ones >= len(lines) // 2 else "0")

    a = to_decimal(most_common_bits)
    b = to_decimal(reverse_binary(most_common_bits))
    return a * b

def filter_lines(lines, is_most_common_strategy = True, index = 0):
    if not lines:
        return 0
    if len(lines) == 1:
        return to_decimal(lines[0])

    ones = [line for line in lines if line[index] == "1"]
    zeroes = [line for line in lines if line[index] == "0"]
    most_common, least_common = (ones, zeroes) if len(ones) >= len(zeroes) else (zeroes, ones)

    if not is_most_common_strategy:
        most_common, least_common = least_common, most_common

    return filter_lines(most_common, is_most_common_strategy, index + 1)

def get_second(lines):
    a = filter_lines(lines, is_most_common_strategy=True)
    b = filter_lines(lines, is_most_common_strategy=False)
    return a * b

if __name__ == '__main__':
    run(get_first, get_second)
