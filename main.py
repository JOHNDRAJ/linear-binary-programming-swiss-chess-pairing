from optimization.primary_optimization import solve_pairing_problem
from utils.import_data import add_edges_from_optimized_csv
from utils.export_data import export_node_pair_info_to_csv
from utils.tests import test_pairs
from utils.simulate_scenarios import add_weighted_edges
from utils.visulize_data import transform_csv_data
import networkx as nx
import numpy as np
import csv
import os
import random
import names
from visualize_dictionary import plot_dict


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
#names = ['Alice', 'Ben', 'Charlotte', 'David', 'Emma', 'Fiona', 'Grace', 'Hannah', 'Isaac', 'Julia']
# names = [('Alice', 1200), ('Ben', 1300), ('Charlotte', 1400), ('David', 1500), ('Emma', 1600), ('Fiona', 1700), ('Grace', 1800), ('Hannah', 1900), ('Isaac', 2000), ('Julia', 2100)]

def generate_names(size, min_num, max_num):
    unique_first_names = set()
    result = []
    schoolList = ['AG', 'SLO', 'Templton']
    mean = (min_num + max_num) / 2
    std_dev = (max_num - min_num) / 6  # Choose a standard deviation that covers most of the range

    # Keep generating names until we have the desired number of unique names
    while len(unique_first_names) < size:
        first_name = names.get_first_name()
        school = random.choice(schoolList)
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            # Generate a random number with a normal distribution and clip it to the range
            random_number = int(np.clip(np.random.normal(mean, std_dev), min_num, max_num))
            result.append((first_name, random_number, school))
    
    return result

labels = generate_names(100, 500, 2000)

# Create a graph
adjacency_matrix = np.zeros((len(labels),len(labels)))
G = nx.from_numpy_array(adjacency_matrix,create_using=nx.DiGraph)

# Add labels as node attributes
for i, (name, rating, school) in enumerate(labels):
    G.nodes[i]['label'] = name
    G.nodes[i]['rating'] = rating
    G.nodes[i]['matchHistory'] = []
    G.nodes[i]['colorNum'] = 0
    G.nodes[i]['color'] = None
    G.nodes[i]['colorStreak'] = 1
    G.nodes[i]['school'] = school
    G.nodes[i]['score'] = 0


dataList = []

weightDiffList = []

sdDict = {}

ratingOutcomeDict = {}

durations = ['full', 3, 'full', 'full']
for i in range(5):
    #score, rating, color, school
    pairs, scores, sameSchoolNum = solve_pairing_problem(G, durations[0], durations[1], durations[2], durations[3])
    for i in range(len(durations)):
        if isinstance(durations[i], int) and durations[i] > 0:
            durations[i] -= 1

    for (j,k) in pairs:
        scoreDiff = abs(scores[j] - scores[k])
        ratingDiff = abs(G.nodes[j]['rating'] - G.nodes[k]['rating'])
        weightDiffList.append((scoreDiff, ratingDiff))
        if scoreDiff in sdDict:
            sdDict[scoreDiff] += 1
        else:
            sdDict[scoreDiff] = 1
        print(ratingDiff)

    
    

    test_pairs(G, pairs)

    add_weighted_edges(G, pairs)

    filename = 'data/new_node_pair_info_sim'+str(i)+'.csv'

    export_node_pair_info_to_csv(G, pairs, filename)

    dataList.append(transform_csv_data(filename))
    
for i in dataList:
    print(i)
    print('\n')

def round_to_nearest_50(num):
    return round(num / 50) * 50

scoreDiffMean = sum([i for (i,j) in weightDiffList])/len(weightDiffList)
ratingDiffMean = sum([j for (i,j) in weightDiffList])/len(weightDiffList)
colorNumberMean = sum([G.nodes[i]['colorNum'] for i in G.nodes])/len(G.nodes)

maxImbalance = 0
numImbalances = 1
for i in G.nodes:
    if G.nodes[i]['colorNum'] > maxImbalance:
        maxImbalance = G.nodes[i]['colorNum']
        numImbalances = 1
    elif G.nodes[i]['colorNum'] == maxImbalance:
        numImbalances += 1

    outcome = round_to_nearest_50(G.nodes[i]['rating'])
    if outcome not in ratingOutcomeDict:
        ratingOutcomeDict[outcome] = [G.nodes[i]['score']]
    else:
        ratingOutcomeDict[outcome].append(G.nodes[i]['score'])
ratingOutcomeDict = {key: ratingOutcomeDict[key] for key in sorted(ratingOutcomeDict)}

    


maxStreak = 0
numStreaks = 1
for i in G.nodes:
    if G.nodes[i]['colorStreak'] > maxStreak:
        maxStreak = G.nodes[i]['colorStreak']
        numStreaks = 1
    elif G.nodes[i]['colorStreak'] == maxStreak:
        numStreaks += 1

print(f"Average score difference: {scoreDiffMean}")
print(f"Average rating difference: {ratingDiffMean}")
# print(f"Average color balance: {colorNumberMean}") #positive is white, negative is black
print(f"Largest single color imbalance: {maxImbalance}, {numImbalances} times")
print(f"Largest color streak: {maxStreak}, {numStreaks} times")
print(f"Schools played themselves {sameSchoolNum} times")

sdDict = {key: sdDict[key] for key in sorted(sdDict)}
for i in sdDict:
    print(f"{i} Score diff: {sdDict[i]} times")

print("Rating outcome distribution mean:")
for i in ratingOutcomeDict:

    # print(f"{i}:{sum(ratingOutcomeDict[i])/len(ratingOutcomeDict[i])}")
    ratingOutcomeDict[i] = [sum(ratingOutcomeDict[i])/len(ratingOutcomeDict[i])]


plot_dict(ratingOutcomeDict)

