from aoc import run, get_int_numbers
from collections import namedtuple

Point = namedtuple('Point', 'x, y')
Velocity = namedtuple('Velocity', 'dx, dy')
Target = namedtuple('Target', 'x_min, x_max, y_min, y_max')

def get_input_as_target(lines):
    [x_min, x_max, y_min, y_max] = get_int_numbers(lines[0])
    return Target(x_min, x_max, y_min, y_max)

def get_sum(n):
    return (n * (n + 1)) // 2 if n > 0 else 0

def is_point_in_target(point, target):
    return target.x_min <= point.x <= target.x_max and target.y_min <= point.y <= target.y_max

def is_point_after_target(point, target):
    return point.x > target.x_max or point.y < target.y_min

def is_valid_trajectory(start_point, velocity, target):
    point = start_point
    while True:
        point = Point(point.x + velocity.dx, point.y + velocity.dy)
        if is_point_in_target(point, target):
            return True
        if is_point_after_target(point, target):
            return False
        velocity = Velocity(max(0, velocity.dx - 1), velocity.dy - 1)

def iter_trajectory_velocities(start_point, target):
    max_x = target.x_max + 1
    min_y = target.y_min - 1
    max_y = abs(target.y_min) + 1

    for x in range(1, max_x + 1):
        for y in range(min_y, max_y + 1):
            velocity = Velocity(x, y)
            if is_valid_trajectory(start_point, velocity, target):
                yield velocity

def get_first(lines):
    target = get_input_as_target(lines)
    return max(get_sum(v.dy) for v in iter_trajectory_velocities(Point(0, 0), target))

def get_second(lines):
    target = get_input_as_target(lines)
    return len(list(iter_trajectory_velocities(Point(0, 0), target)))

if __name__ == '__main__':
    run(get_first, get_second)
