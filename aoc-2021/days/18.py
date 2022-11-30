from aoc import run
from collections import deque
from functools import reduce
from math import floor, ceil
from itertools import product

class BinaryNode:
    def __init__(self, value = None):
        self.value = value
        self.parent = None
        self._left = None
        self._right = None

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        if self._left:
            self._left.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if self._right:
            self._right.parent = self

    def is_leaf(self):
        return self.left is None and self.right is None

    def iter_parents(self):
        if not self.parent:
            return
        yield self.parent
        yield from self.parent.iter_parents()

    def find_inorder_node(self, func):
        left_node = self.left.find_inorder_node(func) if self.left else None
        if left_node:
            return left_node

        if func(self):
            return self

        right_node = self.right.find_inorder_node(func) if self.right else None
        if right_node:
            return right_node

    def find_after_leaf_node(self):
        parent_node = self.parent
        child_node = self
        while True:
            if not parent_node:
                break
            if parent_node.right and parent_node.right != child_node:
                break
            child_node = parent_node
            parent_node = parent_node.parent

        if not parent_node:
            return None

        after_node = parent_node.right
        while not after_node.is_leaf():
            after_node = after_node.left
        return after_node

    def find_before_left_node(self):
        parent_node = self.parent
        child_node = self
        while True:
            if not parent_node:
                break
            if parent_node.left and parent_node.left != child_node:
                break
            child_node = parent_node
            parent_node = parent_node.parent

        if not parent_node:
            return None

        before_node = parent_node.left
        while not before_node.is_leaf():
            before_node = before_node.right
        return before_node


class SnailFishNumber(BinaryNode):

    def is_for_explode(self):
        return not self.is_leaf() and self.left.is_leaf() and self.right.is_leaf() and len(list(self.iter_parents())) >= 4

    def is_for_split(self):
        return self.is_leaf() and self.value >= 10

    def explode(self):
        before_leaf_node = self.find_before_left_node()
        if before_leaf_node:
            before_leaf_node.value += self.left.value

        after_leaf_node = self.find_after_leaf_node()
        if after_leaf_node:
            after_leaf_node.value += self.right.value

        self.left = None
        self.right = None
        self.value = 0

    def split(self):
        self.left = SnailFishNumber(floor(self.value / 2))
        self.right = SnailFishNumber(ceil(self.value / 2))
        self.value = None

    def reduce(self):
        explode_node = self.find_inorder_node(lambda n: n.is_for_explode())
        if explode_node:
            explode_node.explode()
            return self.reduce()

        split_node = self.find_inorder_node(lambda n: n.is_for_split())
        if split_node:
            split_node.split()
            return self.reduce()

    def get_magnitude(self):
        if self.is_leaf():
            return self.value
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

    def __add__(self, other_number):
        if not isinstance(other_number, SnailFishNumber):
            raise Exception(f'Expected SnailFishNumber, not {str(other_number)}')

        new_number = SnailFishNumber()
        new_number.left = self
        new_number.right = other_number
        new_number.reduce()
        return new_number

    @staticmethod
    def from_str(line):
        stack = deque()

        for char in line:
            if char == '[':
                stack.append(SnailFishNumber())
            if char.isdigit():
                stack.append(SnailFishNumber(int(char)))
            if char == ']':
                right = stack.pop()
                left = stack.pop()
                parent = stack.pop()
                parent.left = left
                parent.right = right
                stack.append(parent)

        return stack.pop()

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return f'[{str(self.left)},{str(self.right)}]'

    def __repr__(self):
        return str(self)

def get_first(lines):
    n = reduce(lambda a, b: a + b, (SnailFishNumber.from_str(line) for line in lines))
    return n.get_magnitude()

def get_second(lines):
    max_magnitude = 0
    for line1, line2 in product(lines, lines):
        if line1 == line2:
            continue
        result = SnailFishNumber.from_str(line1) + SnailFishNumber.from_str(line2)
        max_magnitude = max(max_magnitude, result.get_magnitude())
    return max_magnitude

if __name__ == '__main__':
    run(get_first, get_second)
