from aoc import run

def iter_number_batches(lines):
    batch = []
    for line in lines:
        if line:
            batch.append(int(line))
            continue

        if batch:
            yield batch
            batch = []

    if batch:
        yield batch

def get_first(lines):
    sums = (sum(batch) for batch in iter_number_batches(lines))
    return max(sums)

def get_second(lines):
    sums = (sum(batch) for batch in iter_number_batches(lines))
    return sum(sorted(sums, reverse=True)[:3])

if __name__ == '__main__':
    run(get_first, get_second)
