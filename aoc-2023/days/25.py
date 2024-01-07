from aoc import run
from operator import mul
from functools import reduce
from collections import deque
from typing import List, Dict, Set, Tuple, Union

class Node:
    def __init__(self, name: str):
        self.name = name
        self.next_nodes: Set['Node'] = set()
        self.edges: Set['Edge'] = set()

    def connect(self, node: 'Node'):
        edge = Edge(self, node)
        if node not in self.next_nodes:
            self.next_nodes.add(node)
            self.edges.add(edge)
        if self not in node.next_nodes:
            node.next_nodes.add(self)
            node.edges.add(edge)

    def disconnect(self, node: 'Node'):
        edge = Edge(self, node)
        node.next_nodes.remove(self)
        node.edges.remove(edge)
        self.next_nodes.remove(node)
        self.edges.remove(edge)

    def __repr__(self) -> str:
        return f"Node('{self.name}')"

    def __eq__(self, other):
        return isinstance(other, Node) and other.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)

class Edge:
    def __init__(self, start: Node, end: Node):
        start, end = (start, end) if start.name < end.name else (end, start)
        self.start = start
        self.end = end
        self.name = f'{self.start.name}-{self.end.name}'

    def __repr__(self) -> str:
        return f"Edge({self.start}, {self.end})"

    def __eq__(self, other):
        return isinstance(other, Edge) and other.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)

def parse_input(lines: List[str]):
    node_by_name: Dict[str, Node] = dict()
    for line in lines:
        start, ends = line.split(':', maxsplit=1)
        for end in ends.strip().split(' '):
            if start not in node_by_name:
                node_by_name[start] = Node(start)
            if end not in node_by_name:
                node_by_name[end] = Node(end)
            node_by_name[start].connect(node_by_name[end])
    return node_by_name

def get_components(nodes: List[Node]) -> List[List[Node]]:
    visited_nodes: Set[Node] = set()
    components: List[List[Node]] = []
    for start_node in nodes:
        if start_node in visited_nodes:
            continue

        q = deque([start_node])
        component: List[Node] = []

        while q:
            node = q.popleft()
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            component.append(node)
            for next_node in node.next_nodes:
                q.append(next_node)
        components.append(component)

    return components

def get_shortest_paths(nodes: List[Node], start_node: Node):
    visited_nodes: List[Node] = []
    predecessors_by_node: Dict[Node, List[Node]] = {node: [] for node in nodes}
    dist_by_node: Dict[Node, int] = {}
    sigma_by_node: Dict[Node, float] = dict.fromkeys(nodes, 0.0)
    sigma_by_node[start_node] = 1.0
    dist_by_node[start_node] = 0
    q = deque([start_node])

    while q:
        node = q.popleft()
        visited_nodes.append(node)
        curr_dist = dist_by_node[node]
        curr_sigma = sigma_by_node[node]
        for next_node in node.next_nodes:
            if next_node not in dist_by_node:
                q.append(next_node)
                dist_by_node[next_node] = curr_dist + 1
            if dist_by_node[next_node] == curr_dist + 1:
                sigma_by_node[next_node] += curr_sigma
                predecessors_by_node[next_node].append(node)
    return visited_nodes, predecessors_by_node, sigma_by_node, dist_by_node

def accumulate_edges(
    betweenness_by_obj: Dict[Union[Node, Edge], float],
    visited_nodes: List[Node],
    predecessors_by_node: Dict[Node, List[Node]],
    sigma_by_node: Dict[Node, float],
    start_node: Node,
) -> Dict[Union[Node, Edge], float]:
    delta_by_node: Dict[Node, float] = dict.fromkeys(visited_nodes, 0)

    while visited_nodes:
        node = visited_nodes.pop()
        coeff = (1 + delta_by_node[node]) / sigma_by_node[node]

        for prev_node in predecessors_by_node[node]:
            c = sigma_by_node[prev_node] * coeff
            betweenness_by_obj[Edge(prev_node, node)] += c
            delta_by_node[prev_node] += c
        if node != start_node:
            betweenness_by_obj[node] += delta_by_node[node]

    return betweenness_by_obj

def get_edge_betweenness_centrality(
    nodes: List[Node],
) -> List[Tuple[float, Edge]]:
    betweenness_by_obj: Dict[Union[Node, Edge], float] = dict()
    for node in nodes:
        betweenness_by_obj[node] = 0.0
        for edge in node.edges:
            betweenness_by_obj[edge] = 0.0

    for node in nodes:
        visited_nodes, predecessors_by_node, sigma_by_node, _ = get_shortest_paths(
            nodes,
            node,
        )
        betweenness_by_obj = accumulate_edges(
            betweenness_by_obj,
            visited_nodes,
            predecessors_by_node,
            sigma_by_node,
            node,
        )

    scored_edges: List[Tuple[float, Edge]] = [
        (score, obj)
        for obj, score
        in betweenness_by_obj.items()
        if isinstance(obj, Edge)
    ]
    return sorted(scored_edges, key=lambda e: e[0], reverse=True)

def get_first(lines):
    node_by_name = parse_input(lines)
    scored_edges = get_edge_betweenness_centrality(node_by_name.values())
    for _, edge in scored_edges[:3]:
        edge.start.disconnect(edge.end)

    components = get_components(node_by_name.values())
    return reduce(mul, [len(c) for c in components])

if __name__ == '__main__':
    run(get_first)
