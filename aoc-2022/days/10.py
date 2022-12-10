from aoc import run

def parse_line(line):
    parts = line.split(' ', maxsplit=1)
    return int(parts[1]) if len(parts) > 1 else None

def get_array_value(array, index):
    return array[index] if index < len(array) else array[-1]

def get_samples(ops, start_value=1):
    value = start_value
    samples = [value]

    for op in ops:
        if op is None:
            samples.append(value)
        else:
            samples.extend((value, value))
            value += op

    return samples

def iter_crt_lines(samples, width=40, height=6):
    for row in range(height):
        crt_line = []
        for col in range(width):
            cycle = row * width + col + 1
            value = get_array_value(samples, cycle)

            crt_value = '#' if value -1 <= col <= value + 1 else '.'
            crt_line.append(crt_value)

        yield ''.join(crt_line)

def get_first(lines):
    ops = [parse_line(line) for line in lines]
    samples = get_samples(ops)

    indexes = [20, 60, 100, 140, 180, 220]
    return sum(index * get_array_value(samples, index) for index in indexes)

def get_second(lines):
    ops = [parse_line(line) for line in lines]
    samples = get_samples(ops)

    crt_output = '\n'.join(iter_crt_lines(samples))
    print(crt_output)
    return 0

if __name__ == '__main__':
    run(get_first, get_second)
