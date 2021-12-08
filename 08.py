from aoc import run

def parse_input_elements(line):
    return [l.strip() for l in line.split(' ') if l]

def parse_input(line):
    parts = line.split('|')
    return parse_input_elements(parts[0]), parse_input_elements(parts[1])

def get_codes_by_len(codes, n):
    yield from (set(code) for code in codes if len(code) == n)

def get_number_codes(codes):
    numbers = [set()] * 10
    numbers[1] = next(get_codes_by_len(codes, 2))
    numbers[7] = next(get_codes_by_len(codes, 3))
    numbers[4] = next(get_codes_by_len(codes, 4))
    numbers[8] = next(get_codes_by_len(codes, 7))

    five_len_codes = list(get_codes_by_len(codes, 5))
    six_len_codes = list(get_codes_by_len(codes, 6))
    numbers[6] = next(c for c in six_len_codes if not numbers[1].issubset(c))
    numbers[3] = next(c for c in five_len_codes if numbers[1].issubset(c))

    side_left_codes = numbers[8].difference(numbers[3])
    numbers[0] = next(c for c in six_len_codes if side_left_codes.issubset(c) and c != numbers[6])
    numbers[9] = next(c for c in six_len_codes if c != numbers[0] and c != numbers[6])

    top_right_codes = numbers[8].difference(numbers[6])
    numbers[2] = next(c for c in five_len_codes if top_right_codes.issubset(c) and c != numbers[3])
    numbers[5] = next(c for c in five_len_codes if c != numbers[2] and c != numbers[3])

    return numbers

def get_output_number(output_codes, number_codes):
    output_digits = []
    for output_code in output_codes:
        digit = next(index for index, number_code in enumerate(number_codes) if number_code == set(output_code))
        output_digits.append(digit)
    return int("".join(map(str, output_digits)))

def get_first(lines):
    codes = [parse_input(line) for line in lines]
    unique_codes_lens = {2, 3, 4, 7}
    unique_codes_count = 0
    for _, output_codes in codes:
        unique_codes_count += sum(len(c) in unique_codes_lens for c in output_codes)
    return unique_codes_count

def get_second(lines):
    codes = [parse_input(line) for line in lines]
    score = 0
    for input_codes, output_codes in codes:
        number_codes = get_number_codes(input_codes)
        score += get_output_number(output_codes, number_codes)
    return score

if __name__ == '__main__':
    run(get_first, get_second)
