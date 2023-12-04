from aoc import run, get_int_numbers

def parse_line(line: str):
    _, numbers = line.split(':', maxsplit=1)
    winning, current = numbers.split('|', maxsplit=1)
    return get_int_numbers(winning), get_int_numbers(current)

def get_wins_by_card(card):
    winning_numbers, current_numbers = card
    is_winning_used = [False] * len(winning_numbers)
    for number in current_numbers:
        for i, winning_number in enumerate(winning_numbers):
            if number == winning_number and not is_winning_used[i]:
                is_winning_used[i] = True
                break
    return sum(is_winning_used)

def get_first(lines):
    cards = [parse_line(line) for line in lines]
    wins = [get_wins_by_card(card) for card in cards]
    return sum(2**(win - 1) if win else 0 for win in wins)

def get_second(lines):
    cards = [parse_line(line) for line in lines]
    wins = [get_wins_by_card(card) for card in cards]
    counts = [1] * len(wins)
    for i, win in enumerate(wins):
        for j in range(i + 1, i + win + 1):
            counts[j] += counts[i]
    return sum(counts)

if __name__ == '__main__':
    run(get_first, get_second)
