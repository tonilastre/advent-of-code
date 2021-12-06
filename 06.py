from aoc import run, get_int_numbers

def get_counts(numbers, days):
    counts = [0] * 9
    for number in numbers:
        counts[number] += 1

    for day in range(days):
        zeros = counts.pop(0)
        if zeros > 0:
            counts[6] += zeros
        counts.append(zeros)

    return sum(counts)

def get_first(lines):
    numbers = get_int_numbers(lines[0])
    return get_counts(numbers, days=80)

def get_second(lines):
    numbers = get_int_numbers(lines[0])
    return get_counts(numbers, days=256)

if __name__ == '__main__':
    run(get_first, get_second)
