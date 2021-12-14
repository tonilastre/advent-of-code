from aoc import run
from collections import Counter
from functools import lru_cache

CACHE_SIZE = 4096

def parse_input(lines):
    mapping = dict()
    for line in lines:
        if '->' not in line:
            continue
        keys, value = line.split('->')
        mapping[tuple(keys.strip())] = value.strip()
    return lines[0], mapping

def enumerate_pairs(arr):
    for i in range(1, len(arr)):
        yield arr[i - 1], arr[i]

def get_chars_counter(line, mapping, steps):
    @lru_cache(maxsize=CACHE_SIZE)
    def get_counter(two, steps):
        if steps == 0:
            return Counter(two)

        a, b = two
        c = mapping[two]

        mid_counter = Counter({ c: -1 })
        mid_counter.update(get_counter((a, c), steps - 1))
        mid_counter.update(get_counter((c, b), steps - 1))
        return mid_counter

    counter = Counter({ line[0]: 1 })
    for a, b in enumerate_pairs(line):
        counter.update(get_counter((a, b), steps))
        counter.update({ a: -1 })
    return counter

def get_chars_solutions(line, mapping, steps):
    counter = get_chars_counter(line, mapping, steps)
    top, *_, bottom = counter.most_common()
    return top[1] - bottom[1]

def get_first(lines):
    line, mapping = parse_input(lines)
    return get_chars_solutions(line, mapping, 10)

def get_second(lines):
    line, mapping = parse_input(lines)
    return get_chars_solutions(line, mapping, 40)

if __name__ == '__main__':
    run(get_first, get_second)
