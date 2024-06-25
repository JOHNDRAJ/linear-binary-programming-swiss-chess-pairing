from pulp import LpProblem, lpSum, LpMinimize, LpVariable
import networkx as nx
import numpy as np
import random
import csv

def solve_pairing_problem(G):
    # Extract nodes and edges from the original graph
    nodes = list(G.nodes())
    edges = list(G.edges(data='weight'))

    # Calculate scores for each node
    scores = {i: sum(G[i][j]['weight'] for j in G[i]) for i in nodes}

    # Create a new LP problem
    prob = LpProblem("Pairing_Problem", LpMinimize)

    # Create decision variables
    x = {}
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            x[i, j] = LpVariable(f"x_{i}_{j}", cat='Binary')

    # Set objective function
    prob += lpSum(x[i, j] * abs(scores[nodes[i]] - scores[nodes[j]])
                  for i in range(len(nodes)) for j in range(i+1, len(nodes)))

    # Add constraints
    for i in range(len(nodes)):
        prob += lpSum(x[min(i, j), max(i, j)] for j in range(len(nodes)) if i != j) == 1

    for u, v, _ in edges:
        i, j = nodes.index(u), nodes.index(v)
        prob += x[min(i, j), max(i, j)] == 0

    # Solve the problem
    prob.solve()

    # Extract the solution
    pairs = [(nodes[i], nodes[j]) for (i, j) in x if x[i, j].value() == 1]

    return pairs


adjacency_matrix = np.array([
    [0, 0,   0,   0, 0, 1],
    [0, 0,   1.5, 0, 0, 0],
    [0, 1.5, 0,   0, 0, 0],
    [0, 0,   0,   0, 2, 0],
    [0, 0,   0,   1, 0, 0],
    [2, 0,   0,   0, 0, 0]
])


G = nx.from_numpy_array(adjacency_matrix)



pairs = solve_pairing_problem(G)



#%%

def add_weighted_edges(adj_matrix, node_pairs):
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
        
        # Update the adjacency matrix
        adj_matrix[i][j] = weight_ij
        adj_matrix[j][i] = weight_ji
    
    return adj_matrix

def check_paired_once(pairs, num_nodes):
    paired_nodes = [0] * num_nodes
    for i, j in pairs:
        paired_nodes[i] += 1
        paired_nodes[j] += 1
    
    for count in paired_nodes:
        if count != 1:
            print("Test failed: A node is not paired exactly once.")
            return False
    
    return True

def check_no_original_pairs(adjacency_matrix, pairs):
    for i, j in pairs:
        if adjacency_matrix[i, j] > 0 or adjacency_matrix[j, i] > 0:
            print("Test failed: A pair from the original graph is present in the new graph.")
            return False
    
    return True

def test_pairs(adjacency_matrix, pairs):
    num_nodes = adjacency_matrix.shape[0]
    
    # Check if each node is paired exactly once
    if not check_paired_once(pairs, num_nodes):
        return False
    
    # Check if no pairs from the original graph are present in the new graph
    if not check_no_original_pairs(adjacency_matrix, pairs):
        return False
    
    print("All tests passed!")
    return True

# Example usage with the provided pairs

test_result = test_pairs(adjacency_matrix, pairs)


