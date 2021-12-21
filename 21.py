from aoc import run, get_int_numbers
from functools import lru_cache
from collections import Counter
from itertools import product

def get_input_as_positions(lines):
    return [get_int_numbers(line)[-1] for line in lines]

@lru_cache(maxsize=None)
def get_dice_sum_roll_counts(max_number, rolls):
    dice_numbers = list(range(1, max_number + 1))
    dice_roll_combinations = list(product(*[dice_numbers] * rolls))
    dice_sum_counts = Counter(map(sum, dice_roll_combinations))
    return [(dice_sum, roll_count) for dice_sum, roll_count in dice_sum_counts.items()]

def get_new_position_points(positions, points, current_player, movement):
    new_positions = list(positions)
    new_points = list(points)

    new_positions[current_player] = (new_positions[current_player] + movement - 1) % 10 + 1
    new_points[current_player] += new_positions[current_player]

    return tuple(new_positions), tuple(new_points)

@lru_cache(maxsize=None)
def play_complex(positions, points, current_player = 0):
    possible_wins = [p >= 21 for p in points]
    if any(possible_wins):
        return possible_wins

    player_wins = [0, 0]
    for dice_sum, dice_roll_counts in get_dice_sum_roll_counts(max_number = 3, rolls = 3):
        new_positions, new_points = get_new_position_points(
            positions,
            points,
            current_player = current_player,
            movement = dice_sum)
        wins = play_complex(new_positions, new_points, current_player = (current_player + 1) % 2)

        for i, win in enumerate(wins):
            player_wins[i] += win * dice_roll_counts
    return player_wins

def play_simple(positions, points, current_dice = 1, current_player = 0, iteration = 1):
    dices = [(d - 1) % 100 + 1 for d in range(current_dice, current_dice + 3)]
    new_positions, new_points = get_new_position_points(
        positions,
        points,
        current_player = current_player,
        movement = sum(dices))

    if new_points[current_player] >= 1000:
        return new_points, iteration

    return play_simple(
        new_positions,
        new_points,
        current_dice = dices[-1] + 1,
        current_player = (current_player + 1) % 2,
        iteration = iteration + 1)

def get_first(lines):
    player_positions = tuple(get_input_as_positions(lines))
    player_points, iterations = play_simple(player_positions, (0, 0))
    return min(player_points) * iterations * 3

def get_second(lines):
    player_positions = tuple(get_input_as_positions(lines))
    player_wins = play_complex(player_positions, (0, 0))
    return max(player_wins)

if __name__ == '__main__':
    run(get_first, get_second)
