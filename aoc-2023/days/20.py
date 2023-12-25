from aoc import run
from queue import Queue
from operator import mul
from functools import reduce
from abc import ABC, abstractmethod
from typing import List, Dict, Iterator
from collections import namedtuple

Event = namedtuple('Event', 'signal, source, destination')

class Node(ABC):
    def __init__(self, name: str):
        self.name = name
        self.prev_nodes: List['Node'] = []
        self.next_nodes: List['Node'] = []

    @abstractmethod
    def signal(self, signal: int, source: 'Node') -> Iterator[Event]:
        pass

    def add_prev_node(self, node: 'Node'):
        self.prev_nodes.append(node)

    def add_next_node(self, node: 'Node'):
        self.next_nodes.append(node)

    def connect_to(self, destination: 'Node'):
        self.add_next_node(destination)
        destination.add_prev_node(self)

    def __hash__(self):
        return hash(self.name)

class ForwardNode(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def signal(self, signal: int, source: Node) -> Iterator[Event]:
        for node in self.next_nodes:
            yield Event(signal, self, node)

class FlipNode(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.is_on = False

    def signal(self, signal: int, source: Node) -> Iterator[Event]:
        if signal:
            return
        self.is_on = not self.is_on
        new_signal = int(self.is_on)
        for node in self.next_nodes:
            yield Event(new_signal, self, node)

class ConjNode(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.signal_by_source: Dict[Node, int] = {}

    def add_prev_node(self, node: Node):
        self.signal_by_source[node] = 0
        return super().add_prev_node(node)

    def signal(self, signal: int, source: Node) -> Iterator[Event]:
        self.signal_by_source[source] = signal
        new_signal = int(not all(self.signal_by_source.values()))
        for node in self.next_nodes:
            yield Event(new_signal, self, node)

def parse_input(lines):
    node_by_name: Dict[str, Node] = {}
    for line in lines:
        name, _ = line.split(' ', maxsplit=1)
        if name.startswith('%'):
            name = name[1:]
            node_by_name[name] = FlipNode(name)
            continue
        if name.startswith('&'):
            name = name[1:]
            node_by_name[name] = ConjNode(name)
            continue
        node_by_name[name] = ForwardNode(name)

    for line in lines:
        start, ends = line.split('->', maxsplit=1)
        source = start.strip()
        if source.startswith('%') or source.startswith('&'):
            source = source[1:]
        destinations = [d.strip() for d in ends.split(',')]

        source_node = node_by_name[source]
        for destination in destinations:
            destination_node = node_by_name.get(destination)
            if not destination_node:
                destination_node = ForwardNode(destination)
                node_by_name[destination] = destination_node
            source_node.connect_to(destination_node)
    return node_by_name

def get_first(lines):
    node_by_name = parse_input(lines)
    counts = [0, 0]
    for _ in range(1000):
        queue = Queue()
        queue.put(Event(0, None, node_by_name['broadcaster']))

        while not queue.empty():
            signal, source, destination = queue.get()
            counts[signal] += 1
            for event in destination.signal(signal, source):
                queue.put(event)
    return counts[0] * counts[1]

def get_second(lines):
    node_by_name = parse_input(lines)
    rx_node = node_by_name['rx']

    count_by_check_node: Dict[Node, List[int]] = dict()
    for node in rx_node.prev_nodes:
        for prev_node in node.prev_nodes:
            count_by_check_node[prev_node] = []

    count = 0
    while True:
        count += 1
        queue = Queue()
        queue.put(Event(0, None, node_by_name['broadcaster']))

        while not queue.empty():
            signal, source, destination = queue.get()
            if source in count_by_check_node and signal:
                count_by_check_node[source].append(count)

            values = list(count_by_check_node.values())
            if all(values):
                return reduce(mul, (v[0] for v in values))

            for event in destination.signal(signal, source):
                queue.put(event)

if __name__ == '__main__':
    run(get_first, get_second)
