import networkx as nx
from constraint import *

def read_graph(filename):
    return nx.read_edgelist(filename)

def solve_csp(G):
    problem = Problem()

    for node in G.nodes():
        problem.addVariable(node, ['forest', 'dune', 'hill', 'river'])

    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        problem.addConstraint(AllDifferentConstraint(), [node] + neighbors)
        
        if 'forest' in neighbors:
            problem.addConstraint(lambda n, f: n == 'forest' and f == 'hill', [node, 'forest'])

        if 'dune' in neighbors:
            problem.addConstraint(lambda n, d: n == 'dune' and d != 'river', [node, 'dune'])

    solutions = problem.getSolutionIter()

    return solutions

G = read_graph("map.txt")
solutions = solve_csp(G)

count = 0
for solution in solutions:
    print(f"Solution {count+1}:")
    for node, value in solution.items():
        print(f"{node}: {value}")
    count += 1
    print()

if count == 0:
    print("No solutions found.")
