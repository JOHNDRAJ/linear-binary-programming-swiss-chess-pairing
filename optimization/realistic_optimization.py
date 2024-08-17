from pulp import LpProblem, lpSum, LpMinimize, LpMaximize, LpVariable, PULP_CBC_CMD, LpStatus
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

def find_lowest_node(G, score_groups):
    """
    Finds the node with the lowest rating where 'byeStatus' is 0,
    starting from the lowest key in the dictionary and moving up.

    Parameters:
    node_dict (dict): Dictionary where keys are numbers and values are lists of nodes.

    Returns:
    The node with the lowest rating and 'byeStatus' equal to 0.
    Returns None if no such node is found.
    """
    lowest_rating_node = None
    lowest_rating = float('inf')

    # Iterate through the dictionary sorted by keys (lowest to highest)
    for key in sorted(score_groups.keys()):
        nodes = score_groups[key]
        
        for node in nodes:
            # Check if the node is eligible
            if G.nodes[node]['byeStatus'] == 0:
                # Compare ratings
                if G.nodes[node]['rating'] < lowest_rating:
                    lowest_rating = G.nodes[node]['rating']
                    lowest_rating_node = node

    return lowest_rating_node

def create_score_groups(G, nodes):
    lowest_rated_node = None
    groups = {}
    for node in nodes:
        if G.nodes[node]['score'] in groups:
            groups[G.nodes[node]['score']].append(node)
        else:
            groups[G.nodes[node]['score']] = [node]

    #give bye if odd number of players
    lowest_rating = float('inf')
    lowest_node = None
    if len(nodes) % 2 != 0:
        for key in sorted(groups.keys()):
            for node in groups[key]:
                if G.nodes[node]['byeStatus'] == 0:
                    if G.nodes[node]['rating'] < lowest_rating:
                        lowest_rating = G.nodes[node]['rating']
                        lowest_node = node
            if lowest_node != None:
                groups[key].remove(lowest_node)
                break

        # lowest_group = min(groups.keys())
        # lowest_rated_node = min(groups[lowest_group], key=lambda node: G.nodes[node]['rating'])
        # groups[lowest_group].remove(lowest_rated_node)
    return groups, lowest_node

def create_lp_variables(nodes):
    sorted_nodes = sorted(nodes)
    # print(f"normal {nodes}")
    # print(f"sorted {sorted_nodes}")
    x = {}
    for i in range(len(sorted_nodes) - 1):
        for j in range(i + 1, len(sorted_nodes)):
            x[sorted_nodes[i], sorted_nodes[j]] = LpVariable(f"x_{i}_{j}", cat='Binary')
    # for (i, j) in x:
    #     if i > j:
    #         print(f"{i, j} brother")
    #     else:
    #         print(i, j)
    return x    # dict where keys are edge tuples and values are binary LpVariables

def group_objective_function(G, group_nodes, x):
    prob = LpProblem("Pairing_Within_Score_Group", LpMaximize)

    # Soft constraints
    # 1. Maximize the number of pairs created
    num_pairs = lpSum(x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] for i in range(len(group_nodes)) for j in range(i + 1, len(group_nodes)))

    # # 2. Minimize the ratings of unpaired players
    # unpaired_penalty = lpSum((1 - lpSum(x[min(i, j), max(i, j)] for j in range(len(group_nodes)) if i != j)) * G.nodes[group_nodes[i]]['rating'] for i in range(len(group_nodes)))

    # # 3. Prioritize higher-score players for pairing
    # score_penalty = lpSum((1 - lpSum(x[min(i, j), max(i, j)] for j in range(len(group_nodes)) if i != j)) * G.nodes[group_nodes[i]]['score'] for i in range(len(group_nodes)))

    # Objective: Maximize number of pairs and minimize unpaired penalties and score penalties
    prob += num_pairs # - unpaired_penalty - score_penalty

    return prob

def add_constraints(prob, G, group_nodes, x):
    # Hard constraints
    # 1. No two players can be matched if they have previously been matched
    for i in range(len(group_nodes)):
        for j in range(i + 1, len(group_nodes)):
            if G.has_edge(min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])):
                prob += x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] == 0

    # 2. No player can be matched with multiple players during this pass
    for i in range(len(group_nodes)):
        prob += lpSum(x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] for j in range(len(group_nodes)) if i != j) <= 1

def solve_group_pairing(G, group_nodes):
    # Create decision variables
    x = create_lp_variables(group_nodes)

    # Create the objective function
    prob = group_objective_function(G, group_nodes, x)
    
    # Add constraints
    add_constraints(prob, G, group_nodes, x)
    
    # Solve the problem
    prob.solve(PULP_CBC_CMD(msg=False))
    
    match_list = [(i, j) for (i, j) in x if x[i, j].value() == 1]
    new_group = []
    for (i, j) in match_list:
        new_group += [i, j]
    unpaired_players = []
    for i in group_nodes:
        if i not in new_group:
            unpaired_players += [i]

    # unpaired_players = [node for node in group_nodes if lpSum(x[min(node, j), max(node, j)].value() for j in group_nodes if node != j) == 0]
    # unpaired_players = [group_nodes[i] for i in range(len(group_nodes)) if lpSum(x[group_nodes[min(i, j)], group_nodes[max(i, j)]].value() for j in range(len(group_nodes)) if i != j) == 0]
    # print(match_list)
    return match_list, unpaired_players

    # Extract the solution
    # match_list = [(group_nodes[i], group_nodes[j]) for (i, j) in x if x[i, j].value() == 1]
    

def update_groups(unpaired_players, score_groups):
    score_groups = dict(sorted(score_groups.items(), key=lambda item: item[0], reverse=True))
    # print(score_groups)
    bumpDowns = []
    for group in score_groups:
        for bump in bumpDowns:
            score_groups[group].append(bump)
        bumpDowns = []
        for i in score_groups[group]:
            if i in unpaired_players:
                bumpDowns.append(i)
            unpaired_players = [j for j in unpaired_players if j != i]
        score_groups[group] = [i for i in score_groups[group] if i not in bumpDowns]
        # print(f"group {score_groups[group]}")

    if bumpDowns:
        lowest_score = min(score_groups.keys()) - 0.5
        score_groups[lowest_score] = bumpDowns

    return score_groups

def plausible_groups(G, score_groups):
    score_groups = dict(sorted(score_groups.items(), key=lambda item: item[0], reverse=True))
    for group in score_groups:
        matches, unpaired_players = solve_group_pairing(G, score_groups[group])
        score_groups = update_groups(unpaired_players, score_groups)
    # print(score_groups)
    for group in score_groups:
        score_groups[group].sort()
    print(f"plausible {score_groups}")
    return score_groups


def upper_lower_objective_function(G, group_nodes, x):
    prob = LpProblem("Maximize_Upper_Lower", LpMaximize)
    sorted_nodes = sorted(group_nodes, key=lambda n: G.nodes[n]['rating'], reverse=True)
    names = [G.nodes[i]['label'] for i in sorted_nodes]
    
    # Change: Generate penalty pairs to ensure upper vs. lower pairings
    pairs_with_penalties = []
    half = len(sorted_nodes) // 2
    for i in range(half):
        j = half + i
        pairs_with_penalties.append(((i, j), 0))  # No penalty for correct upper-lower pairs


    '''potentially solves the upper lower deviation problem'''
    # half = len(sorted_nodes) // 2
    # for i in range(half):
    #     for j in range(half, len(sorted_nodes)):
    #         deviation = abs((j - half) - i)
    #         penalty = deviation * 10  # Higher penalty for greater deviation
    #         pairs_with_penalties.append(((i, j), penalty))

    penalty_term = lpSum(x[min(sorted_nodes[i], sorted_nodes[j]), max(sorted_nodes[i], sorted_nodes[j])] 
                         for (i, j), _ in pairs_with_penalties 
                         if (min(sorted_nodes[i], sorted_nodes[j]), max(sorted_nodes[i], sorted_nodes[j])) in x)
    
    prob += penalty_term

    # for i in x:
    #     print(f"test {i}")
    # Ensure every player is paired with exactly one other player
    for i in range(len(group_nodes)):
        prob += lpSum(x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] 
                      for j in range(len(group_nodes)) if i != j) == 1

    return prob


def generate_penalty_pairs(n, max_deviation=3):
    pairs_with_penalties = []
    for i in range(n):
        for j in range(i + 1, min(n, i + max_deviation + 1)):
            deviation = j - i
            penalty = deviation * 2  # Higher deviation means higher penalty
            pairs_with_penalties.append(((i, j), penalty))
    return pairs_with_penalties

def solve_upper_lower_pairing(G, group_nodes, score_groups):
    
    keys = sorted(score_groups.keys())
    current_key = next(key for key, val in score_groups.items() if val == group_nodes)
    # print(f"keys: {keys}")
    # print(f"current_key: {current_key}")
    if keys.index(current_key) < len(keys) - 1:
        next_key = keys[keys.index(current_key) + 1]

    if len(group_nodes) <= 1:
        return (group_nodes), current_key

    # Create decision variables
    x = create_lp_variables(group_nodes)

    # Create the objective function
    prob = upper_lower_objective_function(G, group_nodes, x)
    
    # Add constraints
    add_constraints(prob, G, group_nodes, x)
    
    # Solve the problem
    prob.solve(PULP_CBC_CMD(msg=False))
    
    # Check the status of the problem
    if LpStatus[prob.status] != 'Optimal':
        if len(keys) < 2:
            raise ValueError("pairing failed in the highest score group")
        print(f"Upper Lower Problem Status: {LpStatus[prob.status]}")
        #at this point i think that the best approach would be to continually move the lowest score groups into the next highest group until a successful pairing is possible
        del score_groups[current_key]
        try:
            print(next_key)
            score_groups[next_key] += group_nodes
        except NameError as e:
            print(f"there is no higher score group to append to: {e}")
        return solve_upper_lower_pairing(G, score_groups[next_key], score_groups)

    # print(group_nodes)
    # for (i, j), var in x.items():
    #     print(var.value())
    match_list = [(i, j) for (i, j) in x if x[i, j].value() == 1]
    print(f"new_match_list: {match_list}")
    return match_list, current_key

def best_UL_outcome(G, score_groups):
    group_match_lists = {}
    groups = list(reversed(sorted(score_groups.keys())))
    initial_score_groups_size = len(score_groups)
    i = 0
    while i < len(score_groups) and len(score_groups) == initial_score_groups_size:     #iterates through every group unless dict changes sizes meaning final score group was reached and needed to be dealt with
        match_list, key = solve_upper_lower_pairing(G, score_groups[groups[i]], score_groups)
        group_match_lists[key] = match_list     #using key so in case final score group need to be moved up
        print(f"\nscore_groups: {score_groups}")
        print(f"group match lists x: {group_match_lists}\n")
        i += 1
    # print(group_match_lists)
    # print(f"score groups: {score_groups}")
    for key in group_match_lists:
        if not any(isinstance(node, tuple) for node in group_match_lists[key]):
            group_match_lists[key] = []
    return group_match_lists

def find_tuple_containing_value(tuples_list, value):
    for tup in tuples_list:
        if value in tup:
            return tup
    return None

def color_objective_function(G, match_list, group_nodes, x):
    print(f"color_nodes: {group_nodes}")
    print(f"match_list: {match_list}")
    for (i, j) in x:
        print(i, j)
    prob = LpProblem("Minimize_Color_Variance", LpMinimize)
    for (a, b) in match_list:
        for i in range(len(group_nodes)):
            for j in range(i + 1, len(group_nodes)):
                # print(f"pair {i, j}")
                if (group_nodes[i] not in (a,b)) and (group_nodes[j] not in (a,b)):
                    if abs(G.nodes[a]['rating'] - G.nodes[group_nodes[i]]['rating']) > 200 or (abs(G.nodes[a]['rating'] - G.nodes[group_nodes[i]]['rating']) > 80 and G.nodes[a]['colorNum'] == G.nodes[group_nodes[i]]['colorNum']):
                        prob += x[min(group_nodes[i], b), max(group_nodes[i], b)] == 0
                        prob += x[min(a, group_nodes[j]), max(a, group_nodes[j])] == 0
                    if abs(G.nodes[b]['rating'] - G.nodes[group_nodes[i]]['rating']) > 200 or (abs(G.nodes[b]['rating'] - G.nodes[group_nodes[i]]['rating']) > 80 and G.nodes[b]['colorNum'] == G.nodes[group_nodes[i]]['colorNum']):
                        prob += x[min(a, group_nodes[i]), max(a, group_nodes[i])] == 0
                        prob += x[min(b, group_nodes[j]), max(b, group_nodes[j])] == 0
                    if abs(G.nodes[a]['rating'] - G.nodes[group_nodes[j]]['rating']) > 200 or (abs(G.nodes[a]['rating'] - G.nodes[group_nodes[j]]['rating']) > 80 and G.nodes[a]['colorNum'] == G.nodes[group_nodes[j]]['colorNum']):
                        prob += x[min(group_nodes[j], b), max(group_nodes[j], b)] == 0
                        prob += x[min(group_nodes[i], a), max(group_nodes[i], a)] == 0
                    if abs(G.nodes[b]['rating'] - G.nodes[group_nodes[j]]['rating']) > 200 or (abs(G.nodes[b]['rating'] - G.nodes[group_nodes[j]]['rating']) > 80 and G.nodes[b]['colorNum'] == G.nodes[group_nodes[j]]['colorNum']):
                        prob += x[min(a, group_nodes[j]), max(a, group_nodes[j])] == 0
                        prob += x[min(group_nodes[i], b), max(group_nodes[i], b)] == 0
    
    colorSamePenalty = lpSum(x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] * abs(G.nodes[group_nodes[i]]['colorNum'] + G.nodes[group_nodes[j]]['colorNum'])
                             for i in range(len(group_nodes)) for j in range(i + 1, len(group_nodes)))
    
    for i in range(len(group_nodes)):
        prob += lpSum(x[min(group_nodes[i], group_nodes[j]), max(group_nodes[i], group_nodes[j])] 
                      for j in range(len(group_nodes)) if i != j) == 1
    
    prob += colorSamePenalty

    return prob

def solve_color_pairing(G, group_nodes, match_list):
    if len(group_nodes) <= 1:
        return (group_nodes)

    # Create decision variables
    x = create_lp_variables(group_nodes)

    # Create the objective function
    prob = color_objective_function(G, match_list, group_nodes, x)
    
    # Add constraints
    add_constraints(prob, G, group_nodes, x)
    
    # Solve the problem
    prob.solve(PULP_CBC_CMD(msg=False))
    
    # Check the status of the problem
    if LpStatus[prob.status] != 'Optimal':
        print(f"Color Problem Status: {LpStatus[prob.status]}")
        return []

    match_list = [(i, j) for (i, j) in x if x[i, j].value() == 1]
    for (i, j) in match_list:
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
    return match_list

def extract_final_solution(G, score_groups, group_match_lists):
    keys_to_delete = [key for key in score_groups if score_groups[key] == []]
    for key in keys_to_delete:
        del score_groups[key]
    keys_to_delete = [key for key in group_match_lists if group_match_lists[key] == []]
    for key in keys_to_delete:
        del group_match_lists[key]


    new_group_match_lists = {}
    assert len(score_groups) == len(group_match_lists)
    for (key1, group_nodes), (key2, match_list) in zip(score_groups.items(), group_match_lists.items()):
        new_group_match_lists[key1] = solve_color_pairing(G, group_nodes, match_list)
    return new_group_match_lists

