from optimization.primary_optimization import solve_pairing_problem
from utils.import_data import add_edges_from_optimized_csv
from utils.export_data import export_node_pair_info_to_csv
from utils.tests import test_pairs
from utils.simulate_scenarios import add_weighted_edges
from utils.visulize_data import visualize_scores
import networkx as nx
import numpy as np
import csv
import os


"""
#%%
# List of names for the nodes
names = ['Alice', 'Ben', 'Charlotte', 'David', 'Emma', 'Fiona', 'Grace', 'Hannah', 'Isaac', 'Julia']

# Create a graph
adjacency_matrix = np.zeros((len(names),len(names)))
G = nx.from_numpy_array(adjacency_matrix,create_using=nx.DiGraph)

# Add labels as node attributes
for i, name in enumerate(names):
    G.nodes[i]['label'] = name
#%%

pairs = solve_pairing_problem(G)

#%%

test_pairs(G, pairs)


#%%

filename = 'data/node_pair_info4.csv'

add_weighted_edges(G, pairs)
#%%

export_node_pair_info_to_csv(G, pairs, filename)

visualize_scores('data/node_pair_info4.csv')
"""

# List of names for the nodes
names = ['Alice', 'Ben', 'Charlotte', 'David', 'Emma', 'Fiona', 'Grace', 'Hannah', 'Isaac', 'Julia']

# Create a graph
adjacency_matrix = np.zeros((len(names),len(names)))
G = nx.from_numpy_array(adjacency_matrix,create_using=nx.DiGraph)

# Add labels as node attributes
for i, name in enumerate(names):
    G.nodes[i]['label'] = name


for i in range(1):

    pairs = solve_pairing_problem(G)

    test_pairs(G, pairs)

    add_weighted_edges(G, pairs)

    filename = 'data/new_node_pair_info_sim'+str(i)+'.csv'

    export_node_pair_info_to_csv(G, pairs, filename)

    visualize_scores('data/new_node_pair_info_sim'+str(i)+'.csv')

