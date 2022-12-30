from math import ceil
from aoc import run, get_int_numbers

class Blueprint:
    def __init__(self, costs):
        self.costs = costs
        self.max_resources = [
            # Max ore is the max for clay, obsidian or geode
            max(c[0] for c in self.costs[1:]),
            # Max clay is the max need for obsidian
            self.costs[2][1],
            # Max obsidian is the max need for geode
            self.costs[3][2],
            # Max geode should be Infinity
            1_000_000_000,
        ]

    def get_robot_pay_options(self, robots, resources, steps):
        for i, cost in enumerate(self.costs):
            if robots[i] >= self.max_resources[i]:
                continue

            resource_payments = [
                (max(robot_cost - resource, 0), robot_needed_count)
                for resource, robot_cost, robot_needed_count
                in zip(resources, cost, robots)
                if robot_cost != 0
            ]

            pay_steps = -1
            is_pay_possible = True

            for resource_needed, robot_needed_count in resource_payments:
                if robot_needed_count == 0:
                    is_pay_possible = False
                    break
                pay_steps = max(pay_steps, ceil(resource_needed / robot_needed_count))

            if is_pay_possible and pay_steps + 1 <= steps:
                yield (i, pay_steps)

def get_max_resource_count(blueprint, robots, resources, steps):
    if steps <= 0:
        return resources[-1]

    pay_options = list(blueprint.get_robot_pay_options(robots, resources, steps))
    if not pay_options:
        return resources[-1] + robots[-1] * steps

    max_count = 0

    for robot_index, steps_needed in pay_options:
        if steps - steps_needed < 0:
            continue

        robot_costs = blueprint.costs[robot_index]

        new_resources = list(resources)
        for i in range(len(new_resources)):
            new_resources[i] = new_resources[i] - robot_costs[i] + robots[i] * (steps_needed + 1)

        new_robots = list(robots)
        new_robots[robot_index] += 1

        new_max_count = get_max_resource_count(
            blueprint,
            tuple(new_robots),
            tuple(new_resources),
            steps - steps_needed - 1,
        )
        max_count = max(max_count, new_max_count)

    return max_count

def parse_input_line(line) -> Blueprint:
    n = get_int_numbers(line)
    return Blueprint([
        (n[1], 0, 0, 0),
        (n[2], 0, 0, 0),
        (n[3], n[4], 0, 0),
        (n[5], 0, n[6], 0),
    ])

def get_first(lines):
    blueprints = [parse_input_line(line) for line in lines]
    final_sum = 0

    for i, blueprint in enumerate(blueprints, start=1):
        resource_count = get_max_resource_count(
            blueprint,
            robots=(1, 0, 0, 0),
            resources=(0, 0, 0, 0),
            steps=24,
        )
        final_sum += i * resource_count

    return final_sum

def get_second(lines):
    blueprints = [parse_input_line(line) for line in lines]
    final_mul = 1

    for i, blueprint in enumerate(blueprints[:3]):
        resource_count = get_max_resource_count(
            blueprint,
            robots=(1, 0, 0, 0),
            resources=(0, 0, 0, 0),
            steps=32,
        )
        final_mul *= resource_count

    return final_mul

if __name__ == '__main__':
    run(get_first, get_second)
