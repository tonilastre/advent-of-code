from aoc import run
from collections import Counter

def has_duplicates(counter: Counter) -> bool:
    most_common = counter.most_common(1)
    return most_common and most_common[0][1] > 1

def get_unique_window_end_index(line: str, window_size: int) -> int:
    window = Counter(line[:window_size])

    if not has_duplicates(window):
        return window_size

    for i in range(window_size, len(line)):
        prev_letter = line[i - window_size]
        next_letter = line[i]

        window.update(next_letter)
        window.subtract(prev_letter)

        if not has_duplicates(window):
            return i + 1

    return len(line) + 1

def get_first(lines):
    return get_unique_window_end_index(lines[0], window_size=4)

def get_second(lines):
    return get_unique_window_end_index(lines[0], window_size=14)

if __name__ == '__main__':
    run(get_first, get_second)
