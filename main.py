from optimization.experimental_optimization import solve_pairing_problem
from utils.import_data import add_edges_from_optimized_csv
from utils.export_data import export_node_pair_info_to_csv
from utils.tests import test_pairs
from utils.simulate_scenarios import add_weighted_edges
from utils.visulize_data import transform_csv_data
from optimization.realistic_optimization import plausible_groups
from optimization.realistic_optimization import best_UL_outcome
from optimization.realistic_optimization import extract_final_solution
from optimization.realistic_optimization import extract_nodes_and_edges
from optimization.realistic_optimization import create_score_groups
import networkx as nx
import numpy as np
import csv
import os
import random
import names
from visualize_dictionary import plot_dict

def load_players_from_csv(file_path):
    players = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, rating = row
            players.append((name, int(rating), "n/a"))
    return players

def generate_names(size, min_num, max_num):
    unique_first_names = set()
    result = []
    schoolList = ['AG', 'SLO', 'Templton']
    mean = (min_num + max_num) / 2
    std_dev = (max_num - min_num) / 6  # Choose a standard deviation that covers most of the range

    # Keep generating names until we have the desired number of unique names
    initial_rating = min_num
    while len(unique_first_names) < size:
        first_name = names.get_first_name()
        school = random.choice(schoolList)
        if first_name not in unique_first_names:
            unique_first_names.add(first_name)
            # Generate a random number with a normal distribution and clip it to the range
            random_number = min_num
            # random_number = int(np.clip(np.random.normal(mean, std_dev), min_num, max_num))
            result.append((first_name, random_number, school))
        min_num += 99
    
    return result

#toggle between generate_names and load_players_from_csv
# labels = generate_names(20, 0, 20)
labels = load_players_from_csv('10 Players Standings Rd 4.xlsx - 10 Players.csv')

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
    G.nodes[i]['byeStatus'] = 0


dataList = []

weightDiffList = []

sdDict = {}

ratingOutcomeDict = {}

durations = ['full', 3, 'full', 'full']


def enter_game_results(G, pairs):
    for i, j in pairs:
        if i == 'BYE':
            G.nodes[j]['score'] += 0.5
            G.add_edge(j, j, weight=1.5)
        elif j == 'BYE':
            G.nodes[i]['score'] += 0.5
            G.add_edge(i, i, weight=1.5)
        else:
            result = input(f"Enter result for {G.nodes[i]['label']} vs {G.nodes[j]['label']} (1 for {G.nodes[i]['label']} win, 0 for {G.nodes[j]['label']} win, 0.5 for draw): ")
            if result == '1':
                G.nodes[i]['score'] += 1
                G.add_edge(i, j, weight=2)
                G.add_edge(j, i, weight=1)
            elif result == '0':
                G.nodes[j]['score'] += 1
                G.add_edge(i, j, weight=1)
                G.add_edge(j, i, weight=2)
            elif result == '0.5':
                G.nodes[i]['score'] += 0.5
                G.nodes[j]['score'] += 0.5
                G.add_edge(i, j, weight=1.5)
                G.add_edge(j, i, weight=1.5)
    return G


for round_num in range(5):  # Or however many rounds you want
    nodes, edges, ratings, colors, schools = extract_nodes_and_edges(G)
    score_groups, lowest_rated_node = create_score_groups(G, nodes)

    updated_groups = plausible_groups(G, score_groups)
    upper_lower_groups = best_UL_outcome(G, updated_groups)
    # final_pairings = upper_lower_groups
    final_pairings = extract_final_solution(G, updated_groups, upper_lower_groups)
    pairs = []
    for group in final_pairings:
        for j in final_pairings[group]:
            pairs.append(j)
    if lowest_rated_node is not None:
        pairs.append((lowest_rated_node, 'BYE'))

    # Print pairings by name
    print(f"Round {round_num + 1} Pairings:")
    for i, j in pairs:
        if j == 'BYE':
            print(f"{G.nodes[i]['label']} has a bye")
        else:
            print(f"{G.nodes[i]['label']} vs {G.nodes[j]['label']}")
    print("\n")  # Add a newline for readability

    # Enter results manually after pairing
    G = enter_game_results(G, pairs)

    # Export results to CSV and process data for visualization
    filename = f'data/new_node_pair_info_round{round_num}.csv'
    export_node_pair_info_to_csv(G, pairs, filename)
    dataList.append(transform_csv_data(filename))
    
for i in dataList:
    print(i)
    print('\n')

def round_to_nearest_50(num):
    return round(num / 50) * 50

# scoreDiffMean = sum([i for (i,j) in weightDiffList])/len(weightDiffList)
# ratingDiffMean = sum([j for (i,j) in weightDiffList])/len(weightDiffList)
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

# print(f"Average score difference: {scoreDiffMean}")
# print(f"Average rating difference: {ratingDiffMean}")
# print(f"Average color balance: {colorNumberMean}") #positive is white, negative is black
print(f"Largest single color imbalance: {maxImbalance}, {numImbalances} times")
print(f"Largest color streak: {maxStreak}, {numStreaks} times")
# print(f"Schools played themselves {sameSchoolNum} times")

sdDict = {key: sdDict[key] for key in sorted(sdDict)}
for i in sdDict:
    print(f"{i} Score diff: {sdDict[i]} times")

print("Rating outcome distribution mean:")
for i in ratingOutcomeDict:

    # print(f"{i}:{sum(ratingOutcomeDict[i])/len(ratingOutcomeDict[i])}")
    ratingOutcomeDict[i] = [sum(ratingOutcomeDict[i])/len(ratingOutcomeDict[i])]


plot_dict(ratingOutcomeDict)


