import networkx as nx
import csv

def add_edges_from_optimized_csv(G, filename):
    """Add weighted, directed edges to the graph G based on the optimized CSV file data."""
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            node_a = row['Node1']
            node_b = row['Node2']
            result = row['Result']

            if result == 'win':
                G.add_edge(float(node_a), float(node_b), weight=2)
                G.add_edge(float(node_b), float(node_a), weight=1)
            elif result == 'loss':
                G.add_edge(node_a, node_b, weight=1)
                G.add_edge(node_b, node_a, weight=2)
            elif result == 'draw':
                G.add_edge(node_a, node_b, weight=1.5)
                G.add_edge(node_b, node_a, weight=1.5)
            else:
                print(f"Unexpected result: {result}")