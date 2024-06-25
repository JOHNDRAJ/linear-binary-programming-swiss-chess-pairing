import pulp
import numpy as np

def create_graph_optimization_problem(adjacency_matrix):
    num_nodes = adjacency_matrix.shape[0]
    V = list(range(num_nodes))
    
    # Calculate Scores
    Scores = np.sum(adjacency_matrix, axis=1)

    # Define the problem
    prob = pulp.LpProblem("GraphPairingOptimization", pulp.LpMinimize)
    
    # Decision variables
    x = pulp.LpVariable.dicts("x", ((i, j) for i in V for j in V if i < j), cat='Binary')

    # Objective function
    prob += pulp.lpSum([x[i, j] * abs(Scores[i] - Scores[j]) for i in V for j in V if i < j])

    # Constraints
    for i in V:
        prob += pulp.lpSum([x[min(i,j), max(i,j)] for j in V if i != j and i < j]) == 1
    
    # No pairs from the original graph
    for i in V:
        for j in V:
            if i != j and adjacency_matrix[i, j] > 0:
                prob += x[min(i, j), max(i, j)] == 0
    
    return prob, x

def solve_graph_optimization_problem(prob):
    # Solve the problem
    prob.solve()
    
    # Check the status
    if pulp.LpStatus[prob.status] == 'Optimal':
        print("Optimal solution found")
    else:
        print("No optimal solution found")
    
    return prob

def extract_solution(x, num_nodes):
    pairs = []
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            if pulp.value(x[i, j]) == 1:
                pairs.append((i, j))
    return pairs

# Example Usage
adjacency_matrix = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
])
prob, x = create_graph_optimization_problem(adjacency_matrix)
prob = solve_graph_optimization_problem(prob)
pairs = extract_solution(x, adjacency_matrix.shape[0])
#print("Pairs:", pairs)

'''
# No pairs from the original graph
for i in range(num_nodes):
    for j in range(i+1, num_nodes):
        if adjacency_matrix[i, j] > 0 or adjacency_matrix[j, i] > 0:
            prob += x[i, j] == 0

'''


#%%

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
