from aoc import get_int_numbers, run

def parse_input(line):
    label, value = line.split(' ', maxsplit=1)
    return label, int(value)

def get_first(lines):
    lines = [parse_input(line) for line in lines]
    forward = sum(value for label, value in lines if label == 'forward')
    depth_up = sum(value for label, value in lines if label == 'up')
    depth_down = sum(value for label, value in lines if label == 'down')

    return forward * (depth_down - depth_up)

def get_second(lines):
    lines = [parse_input(line) for line in lines]
    forward = 0
    depth = 0
    aim = 0
    for label, value in lines:
        if label == 'forward':
            forward += value
            depth += (aim * value)
        if label == 'up':
            aim -= value
        if label == 'down':
            aim += value
    return forward * depth

if __name__ == '__main__':
    run(get_first, get_second)
