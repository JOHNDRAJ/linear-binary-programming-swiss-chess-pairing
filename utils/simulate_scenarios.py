import networkx as nx
import random


def add_weighted_edges(G, node_pairs):
    # Define the weight options
    weight_options = [
        (2, 1),    # Option 1: weight (i,j) as 2 and (j,i) as 1
        (1.5, 1.5),# Option 2: weight (i,j) as 1.5 and (j,i) as 1.5
        (1, 2)     # Option 3: weight (i,j) as 1 and (j,i) as 2
    ]

    # Iterate over each node pair
    for i, j in node_pairs:
        # Randomly choose one of the weight options
        weight_ij, weight_ji = random.choice(weight_options)

        # Update the weights in the graph
        G.add_edge(i, j, weight=weight_ij)
        G.add_edge(j, i, weight=weight_ji)

    return G