import re
from aoc import run, get_int_numbers, batch
from typing import Dict, Tuple, List, Iterator, Union, Set
from collections import namedtuple, defaultdict

Range = namedtuple('Range', 'start, end')

def parse_mappings(lines) -> Dict[Tuple[str, str], List[Tuple[Range, Range]]]:
    current_names = None
    ranges_by_names = defaultdict(list)
    for line in lines:
        header = re.match(r'^(.*?)-to-(.*?) map:$', line)
        if header:
            current_names = header.groups()
            continue
        numbers = get_int_numbers(line)
        if len(numbers) == 3 and current_names:
            destination_start, source_start, length = numbers

            source_range = Range(source_start, source_start + length)
            destination_range = Range(destination_start, destination_start + length)
            ranges_by_names[current_names].append((source_range, destination_range))
    return ranges_by_names

def is_within_range(range: Range, value: Union[int, Range]) -> bool:
    if isinstance(value, int):
        return range.start <= value < range.end
    return is_within_range(range, value.start) and is_within_range(range, value.end - 1)

def intersects_with_range(range1: Range, range2: Range) -> bool:
    return range1.end > range2.start and range1.start < range2.end

def get_mapped_value(ranges: Tuple[Range, Range], value: int) -> int:
    for start_range, end_range in ranges:
        if not is_within_range(start_range, value):
            continue
        diff = value - start_range.start
        return end_range.start + diff
    return value

def get_mapped_range(ranges: Tuple[Range, Range], value: Range) -> Range:
    for start_range, end_range in ranges:
        if not is_within_range(start_range, value):
            continue
        start_diff = value.start - start_range.start
        len_diff = value.end - value.start
        return Range(end_range.start + start_diff, end_range.start + start_diff + len_diff)
    return value

def split_range(range: Range, checkpoints: Set[int]) -> Iterator[Range]:
    checkpoints.update({ range.start, range.end })
    last_start = range.start
    for checkpoint in sorted(checkpoints):
        if checkpoint >= range.end:
            yield Range(last_start, range.end)
            break
        if checkpoint > last_start:
            yield Range(last_start, checkpoint)
            last_start = checkpoint

def get_mapped_ranges(ranges: Tuple[Range, Range], value: Range) -> Iterator[Range]:
    checkpoints: Set[int] = set()
    for start_range, _ in ranges:
        checkpoints.update((start_range.start, start_range.end))
    return [get_mapped_range(ranges, range) for range in split_range(value, checkpoints)]

def get_first(lines):
    values = get_int_numbers(lines[0])
    ranges_by_names = parse_mappings(lines[1:])
    next_name_by_name = {start: end for start, end in ranges_by_names.keys()}

    current_name = 'seed'
    end_name = 'location'

    while current_name != end_name:
        next_name = next_name_by_name.get(current_name)
        if not next_name:
            break

        temp_values = []
        for value in values:
            ranges = ranges_by_names[(current_name, next_name)]
            temp_values.append(get_mapped_value(ranges, value))
        current_name = next_name
        values = temp_values

    return min(values)

def get_second(lines):
    numbers = get_int_numbers(lines[0])
    range_values = [Range(start, start + end) for start, end in batch(numbers, 2)]
    ranges_by_names = parse_mappings(lines[1:])
    next_name_by_name = {start: end for start, end in ranges_by_names.keys()}

    current_name = 'seed'
    end_name = 'location'

    while current_name != end_name:
        next_name = next_name_by_name.get(current_name)
        if not next_name:
            break

        temp_range_values = []
        for range_value in range_values:
            ranges = ranges_by_names[(current_name, next_name)]
            temp_range_values.extend(get_mapped_ranges(ranges, range_value))
        current_name = next_name
        range_values = temp_range_values

    return min(r.start for r in range_values)

if __name__ == '__main__':
    run(get_first, get_second)
