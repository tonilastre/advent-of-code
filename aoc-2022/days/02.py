from aoc import run

def parse_input(line):
    return line.split(' ', maxsplit=1)

def get_score_by_letter(letter):
    baseline_ord = ord('A') if letter < 'X' else ord('X')
    return ord(letter) - baseline_ord + 1

def get_match_outcome(score_a, score_b):
    if score_a == score_b:
        return 0
    is_win_b = score_a % 3 + 1 == score_b
    return 1 if is_win_b else -1

def to_match_score(outcome):
    # Lose: -1 -> 0, Draw: 0 -> 3, Win: 1 -> 6
    return (outcome + 1) * 3

def get_first(lines):
    picks = [parse_input(line) for line in lines]
    scores = [(get_score_by_letter(a), get_score_by_letter(b)) for a, b in picks]

    final_score = 0
    for score_a, score_b in scores:
        final_score += score_b
        final_score += to_match_score(get_match_outcome(score_a, score_b))

    return final_score

def get_second(lines):
    picks = [parse_input(line) for line in lines]
    scores = [(get_score_by_letter(a), get_score_by_letter(b)) for a, b in picks]

    final_score = 0
    for score_a, match_score in scores:
        # -2 to simulate match outcome: -1 (lose), 0 (draw), 1 (win)
        outcome = match_score - 2
        score_b = (score_a + outcome -1) % 3 + 1

        final_score += score_b
        final_score += to_match_score(outcome)

    return final_score

if __name__ == '__main__':
    run(get_first, get_second)
