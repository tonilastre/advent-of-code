import re
import sys
import time
import inspect
from pathlib import Path
from typing import List, Any, Callable, Tuple

_INPUTS_DIR = 'inputs'
_HERE = Path(__file__).parent

def get_numbers(line: str) -> List[str]:
    """Return the string representation of int and float numbers from the text"""
    return re.findall(r'(\-?\d+(?:\.\d+)?)', line)

def get_positive_numbers(line: str) -> List[str]:
    """Return the string representation of positive int and float numbers from the text"""
    return re.findall(r'(\d+(?:\.\d+)?)', line)

def get_int_numbers(line: str, only_positive: bool = False) -> List[int]:
    """Return int numbers from the text"""
    numbers = get_positive_numbers(line) if only_positive else get_numbers(line)
    return [int(n) for n in numbers]

def get_float_numbers(line: str, only_positive: bool = False) -> List[float]:
    """Return float numbers from the text"""
    numbers = get_positive_numbers(line) if only_positive else get_numbers(line)
    return [float(n) for n in numbers]

def run(*functions: Tuple[Callable[[Any], int]]) -> None:
    """Run the problem functions with the defined day problem input"""
    day = inspect.stack()[-1].filename.split('.')[0].split('/')[-1]
    input_file_suffixes = [f'-{arg}' if arg else '' for arg in sys.argv[1:]] if len(sys.argv) > 1 else ['']

    for input_file_suffix in input_file_suffixes:
        print(f'{_as_red("Day " + day)}:')
        lines = _read_problem_input_lines(day, input_suffix=input_file_suffix)
        if lines:
            _run_problem_functions(lines, *functions)

def _as_red(text):
    return f'\u001b[31;1m{text}\u001b[0m'

def _read_problem_input_lines(day: str, input_suffix: str=''):
    input_file_path = _HERE.joinpath(f'../{_INPUTS_DIR}/{day}{input_suffix}.txt')
    if not input_file_path.exists():
        print(f'  [Error] Input file {input_file_path} does not exist!', file=sys.stderr)
        return

    print(f'  [Info] Reading input from {input_file_path}...')
    with input_file_path.open() as f:
        return [l.strip('\n') for l in f.readlines()]

def _run_problem_functions(lines, *functions):
    for index, func in enumerate(functions):
        started_at = time.perf_counter()
        result = func(lines)
        duration = time.perf_counter() - started_at
        print(f'  [Info] Answer {index + 1}: {result:<18} [{duration:>11.6f} sec]')
    print('')

def _iter_problem_names():
    return sorted(str(file.with_suffix('')) for file in _HERE.iterdir() if re.match(r'\d\d.py', file.name))

def _main(args):
    problem_names = [f'{int(arg):02}' for arg in args] if args else _iter_problem_names()
    for problem_name in problem_names:
        problem_module = __import__(problem_name, fromlist=[])

        print(f'{_as_red("Day " + problem_name)}:')
        lines = _read_problem_input_lines(problem_name)
        _run_problem_functions(lines, problem_module.get_first, problem_module.get_second)

if __name__ == '__main__':
    _main(sys.argv[1:])
