Advent of Code 2021
===

* [Advent of Code 2021](https://adventofcode.com/2021)

## Run a day problem

Run a day problem with the following command:

```bash
python {DAY}.py
```

It will automatically use the input file from `inputs/{DAY}.txt`.
If you wish to run custom input, the second argument can be defined,
such as:

```bash
python {DAY}.py mytest
```

It will look for the input file `input/{DAY}-mytest.txt`.

## Run multiple day problems

If you wish to run multiple, or all, day problems, use the
following command:

```bash
python aoc.py [DAY...]
```

Examples:

```bash
python aoc.py     # Runs all problems
python aoc.py 4 5 # Runs 04 and 05 problems
```

## New day problem

1. Create a sample input file `input/{DAY}-sample.txt` with a problem
   sample input.
3. Create an input file `input/{DAY}.txt` with a problem input.
4. Create a problem script: `{DAY}.py` with the following template:

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
