import re
from itertools import product
from collections import namedtuple
from aoc import run, get_int_numbers

Place = namedtuple('Place', 'minutes, room_name')
Room = namedtuple('Room', 'name, value, next_room_names')

def parse_input_as_graph(lines):
    room_by_name = {}

    for line in lines:
        rate = get_int_numbers(line)[0]
        name, *next_room_names = re.findall(r'[A-Z]{2}', line)
        room_by_name[name] = Room(name, rate, next_room_names)

    return room_by_name

def cache_without_first_arg(func):
    cache = {}
    def wrapper(room_by_name, *args):
        cache_key = tuple(tuple(sorted(arg)) if isinstance(arg, (list, set)) else arg for arg in args)
        if cache_key not in cache:
            cache[cache_key] = func(room_by_name, *args)
        return cache[cache_key]
    return wrapper

@cache_without_first_arg
def get_distance(room_by_name, start_name, end_name):
    queue = {start_name}
    visited = set()
    distance = 0

    while queue:
        new_queue = set()
        distance += 1

        for name in queue:
            if name in visited:
                continue
            visited.add(name)
            new_queue.update(room_by_name[name].next_room_names)

        if end_name in new_queue:
            return distance

        queue = new_queue

    raise Exception(f'No path between {start_name} and {end_name}')

@cache_without_first_arg
def get_max_pressure(room_by_name, closed_names, places):
    if not closed_names:
        return 0

    if any(p.minutes <= 0 for p in places):
        return 0

    places = sorted(places, reverse=True)
    max_pressure = 0

    for i, closed_name in enumerate(closed_names):
        # if all(p.room_name == 'AA' for p in places):
        #     print(f'{i}/{len(closed_names)} start with {closed_name}')
        new_places = list(places)
        new_closed_names = closed_names ^ {closed_name}

        distance = get_distance(room_by_name, places[0].room_name, closed_name)
        new_places[0] = Place(new_places[0].minutes - (distance + 1), closed_name)

        released_pressure = room_by_name[closed_name].value * new_places[0].minutes
        pressure = get_max_pressure(room_by_name, new_closed_names, new_places)

        max_pressure = max(max_pressure, pressure + released_pressure)

    return max_pressure

def get_first(lines):
    room_by_name = parse_input_as_graph(lines)
    closed_names = set(room.name for room in room_by_name.values() if room.value != 0)
    return get_max_pressure(room_by_name, closed_names, [Place(30, 'AA')])

def get_second(lines):
    room_by_name = parse_input_as_graph(lines)
    closed_names = set(room.name for room in room_by_name.values() if room.value != 0)
    return get_max_pressure(room_by_name, closed_names, [Place(26, 'AA'), Place(26, 'AA')])

if __name__ == '__main__':
    run(get_first, get_second)
