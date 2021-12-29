from aoc import run, get_int_numbers
import statistics

def get_first(lines):
    numbers = get_int_numbers(lines[0])
    median = int(statistics.median(numbers))
    return sum(abs(num - median) for num in numbers)

def get_sums(n):
    current_sum = 0
    for i in range(n):
        current_sum += i
        yield current_sum

def get_second(lines):
    numbers = get_int_numbers(lines[0])
    min_number, max_number = min(numbers), max(numbers)
    sums = list(get_sums(max_number + 1))

    solutions = (sum(sums[abs(n - i)] for n in numbers) for i in range(min_number, max_number + 1))
    return min(solutions)

if __name__ == '__main__':
    run(get_first, get_second)
