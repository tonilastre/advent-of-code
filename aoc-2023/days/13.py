from aoc import run
from typing import List

def parse_input(lines):
    buffer: List[str] = []
    for line in lines:
        if line:
            buffer.append(line)
            continue
        if buffer:
            yield buffer
            buffer = []
    if buffer:
        yield buffer

def get_diff_count(line1, line2):
    return sum(c1 != c2 for c1, c2 in zip(line1, line2))

def iter_pairwise_index_by_diffs(lines, max_diff_count: int):
    for i in range(len(lines) - 1):
        diff_count = get_diff_count(lines[i], lines[i + 1])
        if diff_count <= max_diff_count:
            yield (i, diff_count)

def get_row_reflection_index(lines, max_diff_limit = 0, max_diff_count = 0):
    for (index, diff) in iter_pairwise_index_by_diffs(lines, max_diff_count=max_diff_count):
        diff_line_count = int(diff > 0)
        is_reflection = True

        for i in range(index + 2, len(lines)):
            j = 2 * index + 1 - i
            if j < 0:
                break
            diff_count = get_diff_count(lines[i], lines[j])
            diff_line_count += int(diff_count > 0)
            if diff_count > max_diff_count:
                is_reflection = False
                break
            if diff_line_count > max_diff_limit:
                break

        if is_reflection and diff_line_count == max_diff_limit:
            return index
    return -1

def transpose_lines(lines):
    new_lines: List[str] = []
    for col in range(0, len(lines[0])):
        new_line: List[str] = []
        for row in range(0, len(lines)):
            new_line.append(lines[row][col])
        new_lines.append(''.join(new_line))
    return new_lines

def get_reflection(pattern, max_diff_limit=0, max_diff_count=0):
    row = get_row_reflection_index(
        pattern,
        max_diff_limit=max_diff_limit,
        max_diff_count=max_diff_count,
    )
    if row != -1:
        return (row, -1)

    transposed_pattern = transpose_lines(pattern)
    col = get_row_reflection_index(
        transposed_pattern,
        max_diff_limit=max_diff_limit,
        max_diff_count=max_diff_count,
    )
    return (-1, col)

def get_first(lines):
    result = 0
    for pattern in parse_input(lines):
        row, col = get_reflection(pattern)
        if row != -1:
            result += (row + 1) * 100
            continue
        if col != -1:
            result += (col + 1)
    return result

def get_second(lines):
    result = 0
    for pattern in parse_input(lines):
        row, col = get_reflection(pattern, max_diff_count=1, max_diff_limit=1)
        if row != -1:
            result += (row + 1) * 100
            continue
        if col != -1:
            result += (col + 1)
    return result

if __name__ == '__main__':
    run(get_first, get_second)
