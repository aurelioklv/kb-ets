import networkx as nx
from networkx.algorithms.coloring import greedy_color


def connected_graph_area(adj_list):
    G = nx.Graph(adj_list)

    components = list(nx.connected_components(G))
    areas = [len(c) for c in components]

    return max(areas)


def shortest_path(G, a, b):
    return nx.shortest_path(G, source=a, target=b)


# Test graph coloring
csp = nx.Graph()
csp.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
csp.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'C'),
                   ('B', 'D'), ('C', 'E'), ('D', 'E')])


def is_valid_coloring(colors):
    for node in csp.nodes:
        for neighbor in csp.neighbors(node):
            if colors[node] == colors[neighbor]:
                return False
    return True


coloring = greedy_color(csp, strategy='largest_first', interchange=True)


if is_valid_coloring(coloring):
    print('Valid coloring:', coloring)
else:
    print('No valid coloring found.')
