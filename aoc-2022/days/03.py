from aoc import run

def get_letter_value(letter):
    baseline_ord = (ord('A') - 26) if letter < 'a' else ord('a')
    return ord(letter) - baseline_ord + 1

def get_first(lines):
    final_value = 0

    for line in lines:
        mid = len(line) // 2
        first_part = set(line[:mid])
        second_part = set(line[mid:])

        for letter in first_part.intersection(second_part):
            final_value += get_letter_value(letter)

    return final_value

def get_second(lines):
    final_value = 0
    group_size = 3

    for i in range(0, len(lines), group_size):
        packages = (set(line) for line in lines[i:i + group_size])
        final_package = next(packages)
        final_package = final_package.intersection(*packages)

        for letter in final_package:
            final_value += get_letter_value(letter)

    return final_value

if __name__ == '__main__':
    run(get_first, get_second)
