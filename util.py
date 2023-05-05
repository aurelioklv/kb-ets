import networkx as nx


def connected_graph_area(graph):
    # graph (adj matrix)
    G = nx.Graph(graph)

    components = list(nx.connected_components(G))
    areas = [len(c) for c in components]

    return max(areas)
