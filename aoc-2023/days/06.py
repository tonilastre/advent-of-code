import re
from aoc import run, get_int_numbers

def get_border_time(time_min, time_max, is_valid):
    if time_min >= time_max:
        return time_max
    time = (time_min + time_max) // 2
    if is_valid(time):
        return get_border_time(time + 1, time_max, is_valid)
    return get_border_time(time_min, time, is_valid)

def get_counts(time, max_distance):
    is_larger = lambda i: (time - i) * i > max_distance
    is_smaller = lambda i: (time - i) * i <= max_distance
    min_time = get_border_time(0, time + 1, is_smaller)
    max_time = get_border_time(0, time + 1, is_larger)
    return max(max_time - min_time, 0)

def get_first(lines):
    times = get_int_numbers(lines[0])
    distances = get_int_numbers(lines[1])

    result = 1
    for time, max_distance in zip(times, distances):
        result *= get_counts(time, max_distance)
    return result

def get_second(lines):
    time = get_int_numbers(re.sub(r'[^\d]', '', lines[0]))[0]
    max_distance = get_int_numbers(re.sub(r'[^\d]', '', lines[1]))[0]
    return get_counts(time, max_distance)

if __name__ == '__main__':
    run(get_first, get_second)
