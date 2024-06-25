from pulp import LpProblem, lpSum, LpMinimize, LpVariable
import networkx as nx
import numpy as np
import random
import csv

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

'''
def check_no_original_pairs(adjacency_matrix, pairs):
    for i, j in pairs:
        if adjacency_matrix[i, j] > 0 or adjacency_matrix[j, i] > 0:
            print("Test failed: A pair from the original graph is present in the new graph.")
            return False
    
    return True
'''

def check_no_original_pairs(G, pairs):
    for u, v in pairs:
        if G.has_edge(u, v) or G.has_edge(v, u):
            print("Test failed: A pair from the original graph is present in the new graph.")
            return False
    
    return True

'''
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
'''


def test_pairs(G, pairs):
    num_nodes = len(G.nodes)
    
    # Check if each node is paired exactly once
    if not check_paired_once(pairs, num_nodes):
        return False
    
    # Check if no pairs from the original graph are present in the new graph
    if not check_no_original_pairs(G, pairs):
        return False
    
    print("All tests passed!")
    return True