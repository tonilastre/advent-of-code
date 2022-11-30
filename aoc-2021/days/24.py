from aoc import run
from typing import Union, Any, List, Optional
from itertools import product

class Operator:
    ADD = 'add'
    MUL = 'mul'
    EQL = 'eql'
    DIV = 'div'
    MOD = 'mod'

    @staticmethod
    def as_sign(operator: str):
        if operator == Operator.ADD:
            return '+'
        if operator == Operator.MUL:
            return '*'
        if operator == Operator.EQL:
            return '=='
        if operator == Operator.DIV:
            return '/'
        if operator == Operator.MOD:
            return '%'
        return '?'

class Number:
    def __init__(self, value: Union[str, int]):
        self.value = int(value)

    def __add__(self, other: Any):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        return other + self

    def __mul__(self, other: Any):
        if isinstance(other, Number):
            return Number(self.value * other.value)
        return other * self

    def __eq__(self, other: Any):
        if isinstance(other, Number):
            return Number(int(self.value == other.value))
        return other == self

    def __floordiv__(self, other: Any):
        if isinstance(other, Number):
            return Number(self.value // other.value)
        return Function(Operator.DIV, self, other)

    def __mod__(self, other: Any):
        if isinstance(other, Number):
            return Number(self.value % other.value)
        return Function(Operator.MOD, self, other)

    def evaluate_possible_values(self):
        return [self.value]

    def evaluate(self, variables):
        return self.value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return str(self)

class Variable:
    def __init__(self, index: int, values: List[int]):
        self.index = index
        self.values = list(values)

    def __add__(self, other: Any):
        if isinstance(other, Number) and other.value == 0:
            return self
        return Function(Operator.ADD, self, other)

    def __mul__(self, other: Any):
        if isinstance(other, Number):
            if other.value == 0:
                return Number(0)
            if other.value == 1:
                return self
        return Function(Operator.MUL, self, other)

    def __eq__(self, other: Any):
        if isinstance(other, Number) and other.value not in self.values:
            return Number(0)
        return Function(Operator.EQL, self, other)

    def __floordiv__(self, other: Any):
        if isinstance(other, Number):
            if other.value == 1:
                return self
            if other.value > max(self.values):
                return Number(0)
        return Function(Operator.DIV, self, other)

    def __mod__(self, other):
        if isinstance(other, Number):
            if other.value > max(self.values):
                return self
        return Function(Operator.MOD, self, value)

    def evaluate_possible_values(self):
        return self.values

    def evaluate(self, variables):
        return variables[self.index]

    def __str__(self):
        return f'x{self.index})'

    def __repr__(self):
        return str(self)

class Function:
    def __init__(self, operator: str, arg1, arg2, skip_eval = True):
        self.operator = operator
        self.arg1 = arg1
        self.arg2 = arg2
        self._variable_indexes = None
        self._variable_indexes = get_variable_indexes(self)
        self._possible_values = None
        if skip_eval:
            self._possible_values = self.evaluate_possible_values()

        # Keeps cached evaluation for variable_indexes to the final result
        self._cached_evaluations = dict()

    def __add__(self, other: Any):
        if isinstance(other, Number) and other.value == 0:
            return self
        return Function(Operator.ADD, self, other)

    def __mul__(self, other: Any):
        if isinstance(other, Number):
            if other.value == 0:
                return Number(0)
            if other.value == 1:
                return self
        return Function(Operator.MUL, self, other)

    def __eq__(self, other: Any):
        func = Function(Operator.EQL, self, other, skip_eval = False)
        if func._possible_values and len(func._possible_values) == 1:
            return Number(func._possible_values[0])
        return func

    def __floordiv__(self, other: Any):
        if isinstance(other, Number) and other.value == 1:
            return self
        func = Function(Operator.DIV, self, other, skip_eval = False)
        if func._possible_values and len(func._possible_values) == 1:
            return Number(func._possible_values[0])
        return func

    def __mod__(self, other: Any):
        func = Function(Operator.MOD, self, other, skip_eval = False)
        if func._possible_values and len(func._possible_values) == 1:
            return Number(func._possible_values[0])
        return func

    def evaluate_possible_values(self):
        if self._possible_values:
            return self._possible_values

        eval_arg1 = self.arg1.evaluate_possible_values()
        eval_arg2 = self.arg2.evaluate_possible_values()

        eval_results = set()
        for arg_combo in product(eval_arg1, eval_arg2):
            arg1, arg2 = arg_combo
            result = evaluate_operator(self.operator, arg1, arg2)
            if result is not None:
                eval_results.add(result)

        return list(eval_results)

    def evaluate(self, variables):
        func_variables = tuple(variables[i] for i in self._variable_indexes)
        if func_variables in self._cached_evaluations:
            return self._cached_evaluations[func_variables]

        eval_arg1 = self.arg1.evaluate(variables)
        eval_arg2 = self.arg2.evaluate(variables)

        if eval_arg1 is None or eval_arg2 is None:
            result = None
        else:
            result = evaluate_operator(self.operator, eval_arg1, eval_arg2)

        self._cached_evaluations[func_variables] = result
        return result

    def __str__(self):
        operator_sign = Operator.as_sign(self.operator)
        return f"({str(self.arg1)} {operator_sign} {str(self.arg2)})"

    def __repr__(self):
        return str(self)

def get_variable_indexes(obj):
    if isinstance(obj, Number):
        return set()
    if isinstance(obj, Variable):
        return set([obj.index])
    if isinstance(obj, Function):
        if obj._variable_indexes:
            return obj._variable_indexes
        s1 = get_variable_indexes(obj.arg1)
        s2 = get_variable_indexes(obj.arg2)
        return s1.union(s2)
    return set()

def evaluate_operator(operator: str, arg1: int, arg2: int) -> Optional[int]:
    if operator == Operator.ADD:
        return arg1 + arg2
    if operator == Operator.MUL:
        return arg1 * arg2
    if operator == Operator.DIV and arg2 != 0:
        return arg1 // arg2
    if operator == Operator.MOD and arg1 >= 0 and arg2 > 0:
        return arg1 % arg2
    if operator == Operator.EQL:
        return int(arg1 == arg2)
    return None

def parse_input_as_function(lines):
    vars = { 'x': Number(0), 'y': Number(0), 'z': Number(0), 'w': Number(0) }
    variable_index = 0

    for i, line in enumerate(lines):
        # print(f'[{i + 1}/{len(lines)}] Parsing line "{line}"...')
        command = line.split(' ')[0]
        if command == 'inp':
            var = line.split(' ')[1]
            vars[var] = Variable(variable_index, list(range(1, 10)))
            variable_index += 1
            continue

        _, var1, var2 = line.split(' ')
        value2 = vars[var2] if var2 in vars else Number(var2)

        if command == Operator.ADD:
            vars[var1] = vars[var1] + value2
        if command == Operator.MUL:
            vars[var1] = vars[var1] * value2
        if command == Operator.DIV:
            vars[var1] = vars[var1] // value2
        if command == Operator.MOD:
            vars[var1] = vars[var1] % value2
        if command == Operator.EQL:
            vars[var1] = vars[var1] == value2

    return vars['z']

def find_valid_input(func: Function, expected_result: int, input_numbers: List[int]):
    """Can be used with `product(range(9, 0, -1), repeat=14)` to iterate"""
    for i, number in enumerate(input_numbers):
        actual_result = func.evaluate(number)
        if actual_result == expected_result:
            yield number

def iter_line_command_values(lines, start_index):
    """Segments in ALU are repeated every 18 lines"""
    for i in range(start_index, len(lines), 18):
        parts = lines[i].split(' ')
        yield int(parts[-1])

def generate_valid_input(lines, get_digit_func):
    """
    ALU steps per digit are:
        1) x = z % 26 + x_add
        2) z = z // (26 or 1) -> 1 if x_add > 9 else 26
        3) z = z * 26 + (DIGIT + y_add) -> if x != DIGIT

    When getting the last digit from z through `z % 26` we want to
    skip adding to the `z`, thus this must be true:
        x == CURRENT_DIGIT
        (z % 26) + x_add == CURRENT_DIGIT
        (LAST_Z_DIGIT + y_add) + x_add == CURRENT_DIGIT
        LAST_Z_DIGIT + y_add = CURRENT_DIGIT - x_add (this is used below)

    With this approach, final `z` will be equal to the starting point
    which is 0.
    """
    z_state = []
    x_adds = list(iter_line_command_values(lines, 5))
    y_adds = list(iter_line_command_values(lines, 15))
    digits = [9] * min(len(x_adds), len(y_adds))

    for digit_i, (x_add, y_add) in enumerate(zip(x_adds, y_adds)):
        # When `x_add` is larger than 9, there is no way for `x + x_add` to be
        # equal to the current digit (1 to 9), so `z` is updated with (digit + y_add)
        if x_add > 9:
            z_state.append((digit_i, y_add))
            continue

        digit_j, j_add = z_state.pop()
        # Equation is: (x[digit_j] + j_add) = (x[digit_i] - x_add), maximize/minimize x[digit_i]
        # print(f'x{digit_i} - {x_add} == x{digit_j} + {j_add}')
        digits[digit_j] = get_digit_func(x_add, j_add)
        digits[digit_i] = digits[digit_j] + j_add + x_add

    return digits

def generate_max_valid_input(lines):
    return generate_valid_input(lines, lambda x_add, y_add: 9 - max(y_add + x_add, 0))

def generate_min_valid_input(lines):
    return generate_valid_input(lines, lambda x_add, y_add: 1 - min(y_add + x_add, 0))

def get_first(lines):
    func_z = parse_input_as_function(lines)
    max_number = generate_max_valid_input(lines)
    # Test if the evaluation equals to 0
    if func_z.evaluate(max_number) != 0:
        return 0
    return int("".join(map(str, max_number)))

def get_second(lines):
    func_z = parse_input_as_function(lines)
    min_number = generate_min_valid_input(lines)
    # Test if the evaluation equals to 0
    if func_z.evaluate(min_number) != 0:
        return 0
    return int("".join(map(str, min_number)))

if __name__ == '__main__':
    run(get_first, get_second)
