from pulp import LpProblem, lpSum, LpMinimize, LpVariable
import networkx as nx
import numpy as np
import random
import csv

def extract_nodes_and_edges(G):
    nodes = list(G.nodes())
    ratings = [G.nodes[node]['rating'] for node in G.nodes()]     #list of string rating
    colors = [G.nodes[node]['colorNum'] for node in G.nodes()]
    schools = [G.nodes[node]['school'] for node in G.nodes()]
    edges = list(G.edges(data='weight'))    #list of tuples : (int node1, int node2, double weight)
    return nodes, edges, ratings, colors, schools

def calculate_scores(G, nodes):
    return {i: sum(G[i][j]['weight'] for j in G[i]) for i in nodes} #dict where keys are int nodes and values are sum of node's game score

def create_lp_variables(nodes):
    x = {}
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            x[i, j] = LpVariable(f"x_{i}_{j}", cat='Binary')
    return x    #dict where keys are edge tuples and values are binary LpVariables

def get_school_difference(school1, school2):
    if school1 == school2:
        return 1
    else:
        return 0

    
def score_normalization_constant(scores, nodes):
    l = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            l.append(abs(scores[nodes[i]] - scores[nodes[j]]))
    if sum(l) != 0:
        return sum(l)
    else:
        return 1
    
def rating_normalization_constant(ratings, nodes):
    l = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            l.append(abs(ratings[i] - ratings[j]))
    if sum(l) != 0:
        return sum(l)
    else:
        return 1
    
def color_normalization_constant(colors, nodes):
    l = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            l.append(abs(colors[i] + colors[j]))
    if sum(l) != 0:
        return sum(l)
    else:
        return 1
    
def school_normalization_constant(schools, nodes):
    l = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            l.append(get_school_difference(schools[i], schools[j]))
    if sum(l) != 0:
        return sum(l)
    else:
        return 1
    


def set_objective_function(prob, x, nodes, scores, ratings, colors, schools, weightScore, weightRating, weightColors, weightSchools):
    scoreDiffPenalty = lpSum(weightScore * x[i, j] * abs(scores[nodes[i]] - scores[nodes[j]]) / score_normalization_constant(scores, nodes)
                             for i in range(len(nodes)) for j in range(i + 1, len(nodes)))
    
    ratingDiffPenalty = lpSum(weightRating * x[i,j] * abs(ratings[i] - ratings[j])
                              for i in range(len(ratings)) for j in range(i+1, len(ratings))) / rating_normalization_constant(ratings, nodes)
    
    #need to add color weighting
    colorSamePenalty = lpSum(weightColors * x[i, j] * abs(colors[i] + colors[j])
                             for i in range(len(nodes)) for j in range(i + 1, len(nodes))) / color_normalization_constant(colors, nodes)
    
    sameSchoolPenalty = lpSum(weightSchools * x[i,j] * get_school_difference(schools[i], schools[j])
                              for i in range(len(nodes)) for j in range(i + 1, len(nodes)))
    
    prob += scoreDiffPenalty + ratingDiffPenalty + colorSamePenalty + sameSchoolPenalty / school_normalization_constant(schools, nodes)
    


def add_constraints(prob, x, nodes, edges):
    #ensures players only paired once
    for i in range(len(nodes)):
        prob += lpSum(x[min(i, j), max(i, j)] for j in range(len(nodes)) if i != j) == 1

    #ensures same players dont play each other twice
    for u, v, _ in edges:
        i, j = nodes.index(u), nodes.index(v)
        prob += x[min(i, j), max(i, j)] == 0

# existing_pairs = []
# def update_existing_pairs(edges, nodes):
#     global existing_pairs
#     existing_pairs = [(nodes.index(u), nodes.index(v)) for u, v, _ in edges]

sameSchoolNum = 0

def extract_solution(G, x, nodes):
    global sameSchoolNum
    matchList = [(nodes[i], nodes[j]) for (i, j) in x if x[i, j].value() == 1]
    for (i, j) in matchList:
        G.nodes[i]['matchHistory'].append(G.nodes[j]['label'])
        G.nodes[j]['matchHistory'].append(G.nodes[i]['label'])
        
        #check for issues here when you add BYE feature
        #if i has more white than j
        if G.nodes[i]['colorNum'] > G.nodes[j]['colorNum']:
            G.nodes[i]['colorNum'] -= 1
            G.nodes[j]['colorNum'] += 1

            if G.nodes[i]['color'] == 'Black':
                G.nodes[i]['colorStreak'] += 1
            else:
                G.nodes[i]['colorStreak'] = 1
            G.nodes[i]['color'] = 'Black'

            if G.nodes[j]['color'] == 'White':
                G.nodes[j]['colorStreak'] += 1
            else:
                G.nodes[i]['colorStreak'] = 1
            G.nodes[j]['color'] = 'White'
            
        #if j has more while than i
        #or
        #if j and i have the same number of white
        else:
            G.nodes[i]['colorNum'] += 1
            G.nodes[j]['colorNum'] -= 1

            if G.nodes[i]['color'] == 'White':
                G.nodes[i]['colorStreak'] += 1
            else:
                G.nodes[i]['colorStreak'] = 1
            G.nodes[i]['color'] = 'White'

            if G.nodes[j]['color'] == 'Black':
                G.nodes[j]['colorStreak'] += 1
            else:
                G.nodes[i]['colorStreak'] = 1
            G.nodes[j]['color'] = 'Black'

        if get_school_difference(G.nodes[i]['school'], G.nodes[j]['school']):
            sameSchoolNum += 1
            




    return matchList 

def solve_pairing_problem(G, scoreWeightDuration, ratingWeightDuration, colorWeightDuration, schoolWeightDuration):
    nodes, edges, ratings, colors, schools = extract_nodes_and_edges(G)
    scores = calculate_scores(G, nodes)
    
    # Create a new LP problem
    prob = LpProblem("Pairing_Problem", LpMinimize)
    
    # Create decision variables
    x = create_lp_variables(nodes)

    # update_existing_pairs(edges, nodes)
    
    # Set objective function
    weights = [3, 0.5, 2, 1]
    weightDurations = [scoreWeightDuration, ratingWeightDuration, colorWeightDuration, schoolWeightDuration]
    for i in range(len(weightDurations)):
        if weightDurations[i] == 0:
            weights[i] = 0
    set_objective_function(prob, x, nodes, scores, ratings, colors, schools, weights[0], weights[1], weights[2], weights[3])
    
    # Add constraints
    add_constraints(prob, x, nodes, edges)
    
    # Solve the problem
    prob.solve()
    
    # Extract the solution
    return extract_solution(G, x, nodes), scores, sameSchoolNum