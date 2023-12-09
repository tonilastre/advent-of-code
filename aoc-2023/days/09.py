from aoc import run, get_int_numbers, pairwise

def iter_numbers(line: str):
    numbers = get_int_numbers(line)
    while any(numbers):
        new_numbers = [num2 - num1 for num1, num2 in pairwise(numbers)]
        yield numbers
        numbers = new_numbers

def get_first(lines):
    result = 0
    for line in lines:
        last_numbers = [numbers[-1] for numbers in iter_numbers(line)]
        result += sum(last_numbers)
    return result

def get_second(lines):
    result = 0
    for line in lines:
        leading_numbers = [numbers[0] for numbers in iter_numbers(line)]

        current = 0
        for num in reversed(leading_numbers):
            current = num - current
        result += current
    return result

if __name__ == '__main__':
    run(get_first, get_second)
