from aoc import run
from typing import Tuple
from collections import Counter

CARDS_COUNT_TYPES = [
    [5],            # five of a kind
    [4, 1],         # four of a kind
    [3, 2],         # full house
    [3, 1, 1],      # three of a kind
    [2, 2, 1],      # two pairs
    [2, 1, 1, 1]    # one pair
]

def parse_line(line):
    cards, amount = line.split(' ', maxsplit=1)
    return cards, int(amount)

def get_cards_count_type(cards: str, is_joker_enabled=False) -> int:
    regular_cards = cards.replace('J', '') if is_joker_enabled else cards
    joker_count = len(cards) - len(regular_cards)

    counter = Counter(regular_cards)
    counts = [value for _, value in counter.most_common()]
    counts = counts or [0]  # for a case of JJJJJ
    counts[0] = counts[0] + joker_count

    for i, cards_count_type in enumerate(CARDS_COUNT_TYPES):
        if counts == cards_count_type:
            return i
    return len(CARDS_COUNT_TYPES)

def get_cards_strength(cards: str, card_values: str, is_joker_enabled=False) -> Tuple[int]:
    card_values = [card_values.index(card) for card in cards]
    return (
        get_cards_count_type(cards, is_joker_enabled=is_joker_enabled),
        *card_values,
    )

def get_total_score(hands):
    return sum(i * amount for i, (_, amount) in enumerate(hands, start=1))

def get_first(lines):
    hands = [parse_line(line) for line in lines]
    strength_by_cards = {
        cards: get_cards_strength(
            cards,
            card_values='AKQJT98765432',
        )
        for cards, _ in hands
    }
    sorted_hands = sorted(
        hands,
        key=lambda hand: strength_by_cards[hand[0]],
        reverse=True,
    )
    return get_total_score(sorted_hands)

def get_second(lines):
    hands = [parse_line(line) for line in lines]
    strength_by_cards = {
        cards: get_cards_strength(
            cards,
            card_values='AKQT98765432J',
            is_joker_enabled=True
        )
        for cards, _ in hands
    }
    sorted_hands = sorted(
        hands,
        key=lambda hand: strength_by_cards[hand[0]],
        reverse=True,
    )
    return get_total_score(sorted_hands)

if __name__ == '__main__':
    run(get_first, get_second)
