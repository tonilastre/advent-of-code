from aoc import run

START_NODE_NAME = 'start'
END_NODE_NAME = 'end'

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = set()

    def connect_to(self, node):
        self.edges.add(node)

    def iter_connected_nodes(self):
        yield from self.edges

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'Node<{self.name}>'

def is_small_node(node):
    return node.name.islower()

def is_end_node(node):
    return node.name == END_NODE_NAME

def is_start_node(node):
    return node.name == START_NODE_NAME

def get_paths_count(node, continue_func = None, visited_nodes = None):
    if is_end_node(node):
        return 1

    new_visited_nodes = dict(visited_nodes or dict())
    new_visited_nodes.setdefault(node, 0)
    new_visited_nodes[node] += 1

    count = 0
    for other_node in node.iter_connected_nodes():
        if continue_func(other_node, new_visited_nodes):
            count += get_paths_count(other_node, continue_func, new_visited_nodes)
    return count

def parse_input_to_graph(lines):
    nodes = dict()
    for line in lines:
        start_name, end_name = line.split('-', maxsplit=1)
        if start_name not in nodes:
            nodes[start_name] = Node(start_name)
        if end_name not in nodes:
            nodes[end_name] = Node(end_name)

        start_node = nodes[start_name]
        end_node = nodes[end_name]

        start_node.connect_to(end_node)
        end_node.connect_to(start_node)
    return nodes

def get_first(lines):
    graph = parse_input_to_graph(lines)

    def continue_func(node, visited_nodes):
        if is_start_node(node):
            return False
        if not is_small_node(node):
            return True
        return node not in visited_nodes

    return get_paths_count(graph[START_NODE_NAME], continue_func=continue_func)

def get_second(lines):
    graph = parse_input_to_graph(lines)

    def continue_func(node, visited_nodes):
        if is_start_node(node):
            return False
        if not is_small_node(node):
            return True
        is_any_double_visit = any(visit_count > 1 for n, visit_count in visited_nodes.items() if is_small_node(n))
        return not (is_any_double_visit and node in visited_nodes)

    return get_paths_count(graph[START_NODE_NAME], continue_func=continue_func)

if __name__ == '__main__':
    run(get_first, get_second)
