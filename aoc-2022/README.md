Advent of Code 2022
===

[Advent of Code 2022](https://adventofcode.com/2022)

## Run a day problem

Run a day problem with the following command:

```bash
python days/{DAY}.py
```

It will automatically use the input file from `inputs/{DAY}.txt`.
If you wish to run custom input, the second argument can be defined,
such as:

```bash
python days/{DAY}.py mytest
```

It will look for the input file `inputs/{DAY}-mytest.txt`.

## Run multiple day problems

If you wish to run multiple, or all, day problems, use the
following command:

```bash
python days/aoc.py [DAY...]
```

Examples:

```bash
python days/aoc.py     # Runs all problems
python days/aoc.py 4 5 # Runs 04 and 05 problems
```

## New day problem

1. Create a sample input file `input/{DAY}-sample.txt` with a problem
   sample input.
3. Create an input file `input/{DAY}.txt` with a problem input.
4. Create a problem script: `days/{DAY}.py` with the following template:

```python
from aoc import run

def get_first(lines):
    # Add solution here...
    return 0

def get_second(lines):
    # Add solution here...
    return 0

if __name__ == '__main__':
    run(get_first, get_second)
```
