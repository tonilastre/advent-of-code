from aoc import run
from itertools import product

def print_image(image):
    for row in image:
        print(''.join(row))

def get_input(lines):
    return lines[0], [list(l) for l in lines[1:] if l]

def enumerate_matrix(matrix):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            yield (i, j), matrix[i][j]

def pixels_to_binary(pixels):
    return ['1' if p == '#' else '0' for p in pixels]

def to_decimal(binary):
    return int("".join(binary), 2) if binary else 0

def iter_window_pixels(matrix, position, default_value = None):
    i, j = position
    for di, dj in product([-1, 0, 1], [-1, 0, 1]):
        new_i = i + di
        new_j = j + dj

        if new_i < 0 or new_i >= len(matrix):
            yield default_value
            continue

        if new_j < 0 or new_j >= len(matrix[0]):
            yield default_value
            continue

        yield matrix[new_i][new_j]

def get_empty_image(rows, cols):
    return list(list('.' * cols) for _ in range(rows))

def enhance_image(image, codes, infinite_value = '.'):
    new_image = get_empty_image(len(image) + 2, len(image[0]) + 2)

    for (i, j), _ in enumerate_matrix(new_image):
        pixels = iter_window_pixels(image, (i - 1, j - 1), default_value = infinite_value)
        code_index = to_decimal(pixels_to_binary(pixels))
        new_image[i][j] = codes[code_index]

    return new_image

def enhance_image_multiple(image, codes, n):
    infinite_value = '.'
    for _ in range(n):
        image = enhance_image(image, codes, infinite_value=infinite_value)
        infinite_code_index = to_decimal(pixels_to_binary([infinite_value] * 9))
        infinite_value = codes[infinite_code_index]
    return image

def get_first(lines):
    codes, image = get_input(lines)
    final_image = enhance_image_multiple(image, codes, 2)
    return sum(value == '#' for _, value in enumerate_matrix(final_image))

def get_second(lines):
    codes, image = get_input(lines)
    final_image = enhance_image_multiple(image, codes, 50)
    return sum(value == '#' for _, value in enumerate_matrix(final_image))

if __name__ == '__main__':
    run(get_first, get_second)
