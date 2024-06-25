from pulp import LpProblem, lpSum, LpMinimize, LpVariable
import networkx as nx
import numpy as np
import random
import csv

def extract_nodes_and_edges(G):
    nodes = list(G.nodes())     #list : int
    edges = list(G.edges(data='weight'))    #list : (node1, node2, weight)
    return nodes, edges

def calculate_scores(G, nodes):
    return {i: sum(G[i][j]['weight'] for j in G[i]) for i in nodes} #dict where keys are int nodes and values are sum of node's game score

def create_lp_variables(nodes):
    x = {}
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x[i, j] = LpVariable(f"x_{i}_{j}", cat='Binary')
    return x    #dict where keys are edge tuples and values are binary LpVariables

def set_objective_function(prob, x, nodes, scores):
    prob += lpSum(x[i, j] * abs(scores[nodes[i]] - scores[nodes[j]])
                  for i in range(len(nodes)) for j in range(i + 1, len(nodes)))

def add_constraints(prob, x, nodes, edges):
    #ensures players only paired once
    for i in range(len(nodes)):
        prob += lpSum(x[min(i, j), max(i, j)] for j in range(len(nodes)) if i != j) == 1

    #ensures same players dont play each other twice
    for u, v, _ in edges:
        i, j = nodes.index(u), nodes.index(v)
        prob += x[min(i, j), max(i, j)] == 0

def extract_solution(x, nodes):
    return [(nodes[i], nodes[j]) for (i, j) in x if x[i, j].value() == 1]   #list of all new pairs

def solve_pairing_problem(G):
    nodes, edges = extract_nodes_and_edges(G)
    scores = calculate_scores(G, nodes)
    
    # Create a new LP problem
    prob = LpProblem("Pairing_Problem", LpMinimize)
    
    # Create decision variables
    x = create_lp_variables(nodes)
    
    # Set objective function
    set_objective_function(prob, x, nodes, scores)
    
    # Add constraints
    add_constraints(prob, x, nodes, edges)
    
    # Solve the problem
    prob.solve()
    
    # Extract the solution
    return extract_solution(x, nodes)