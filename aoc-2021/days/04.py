from collections import defaultdict
from itertools import combinations
from aoc import get_int_numbers, run

BOARD_SIZE = 5

def get_input_board_row(inp):
    return [get_int_numbers(line) for line in inp if line]

def get_input(lines):
    numbers = get_int_numbers(lines[0])
    boards = [get_input_board_row(lines[i:i+BOARD_SIZE+1]) for i in range(1, len(lines), BOARD_SIZE+1)]
    return numbers, boards

def iter_rows(board):
    yield from board

def iter_cols(board):
    for i in range(0, len(board[0])):
        yield [row[i] for row in board]

def get_board_combos(board):
    board_combos = []
    for row in iter_rows(board):
        board_combos.append(set(row))
    for col in iter_cols(board):
        board_combos.append(set(col))
    return board_combos

def is_board_combos_win(board_combos, bingo_numbers):
    return any(board_combo.issubset(bingo_numbers) for board_combo in board_combos)

def iter_board_unchecked_numbers(board, bingo_numbers):
    for row in board:
        yield from (num for num in row if num not in bingo_numbers)

def get_first(lines):
    numbers, boards = get_input(lines)
    boards_combos = [get_board_combos(b) for b in boards]

    for i in range(BOARD_SIZE, len(numbers)):
        bingo_last_number = numbers[i-1]
        bingo_numbers = set(numbers[:i])

        for index, board_combos in enumerate(boards_combos):
            if not is_board_combos_win(board_combos, bingo_numbers):
                continue

            unchecked_sum = sum(iter_board_unchecked_numbers(boards[index], bingo_numbers))
            return unchecked_sum * bingo_last_number

    return 0

def get_second(lines):
    numbers, boards = get_input(lines)
    boards_combos = [get_board_combos(b) for b in boards]
    boards_indexes_won = set()

    for i in range(BOARD_SIZE, len(numbers)):
        bingo_last_number = numbers[i-1]
        bingo_numbers = set(numbers[:i])

        for index, board_combos in enumerate(boards_combos):
            if index in boards_indexes_won:
                continue
            if not is_board_combos_win(board_combos, bingo_numbers):
                continue

            boards_indexes_won.add(index)
            if len(boards_indexes_won) != len(boards):
                continue

            unchecked_sum = sum(iter_board_unchecked_numbers(boards[index], bingo_numbers))
            return unchecked_sum * bingo_last_number

    return 0

if __name__ == '__main__':
    run(get_first, get_second)
