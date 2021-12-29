from aoc import run

def get_first(lines):
    numbers = [int(line) for line in lines]
    return sum(numbers[i + 1] > numbers[i] for i in range(0, len(numbers) - 1))

def get_second(lines):
    numbers = [int(line) for line in lines]
    new_numbers = [sum(numbers[i:i+3]) for i in range(0, len(numbers) - 2)]
    return get_first(new_numbers)

if __name__ == '__main__':
    run(get_first, get_second)
