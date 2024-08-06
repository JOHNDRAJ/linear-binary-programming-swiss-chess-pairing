from pulp import LpProblem, LpMaximize, LpVariable, lpSum
from optimization.realistic_optimization import plausible_groups
from optimization.realistic_optimization import best_UL_outcome
from optimization.realistic_optimization import extract_final_solution
import networkx as nx

# Example usage
G = nx.Graph()  # Assuming G is your graph with node attributes and match history
# Add nodes (players) with attributes
players = [
    # Score 2.5
    (1, {'rating': 1000, 'colorNum': 3, 'school': 'A', 'score': 2.5, 'label': 'Player1', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (2, {'rating': 1050, 'colorNum': 2, 'school': 'B', 'score': 2.5, 'label': 'Player2', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (3, {'rating': 1100, 'colorNum': 1, 'school': 'A', 'score': 2.5, 'label': 'Player3', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (4, {'rating': 1150, 'colorNum': 2, 'school': 'B', 'score': 2.5, 'label': 'Player4', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (5, {'rating': 1200, 'colorNum': 3, 'school': 'A', 'score': 2.5, 'label': 'Player5', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (6, {'rating': 1250, 'colorNum': 2, 'school': 'B', 'score': 2.5, 'label': 'Player6', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (7, {'rating': 1300, 'colorNum': 1, 'school': 'A', 'score': 2.5, 'label': 'Player7', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    # Score 3.0
    (8, {'rating': 1350, 'colorNum': 3, 'school': 'C', 'score': 3.0, 'label': 'Player8', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (9, {'rating': 1400, 'colorNum': 2, 'school': 'B', 'score': 3.0, 'label': 'Player9', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (10, {'rating': 1450, 'colorNum': 1, 'school': 'C', 'score': 3.0, 'label': 'Player10', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (11, {'rating': 1500, 'colorNum': 3, 'school': 'C', 'score': 3.0, 'label': 'Player11', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (12, {'rating': 1550, 'colorNum': 2, 'school': 'B', 'score': 3.0, 'label': 'Player12', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (13, {'rating': 1600, 'colorNum': 1, 'school': 'C', 'score': 3.0, 'label': 'Player13', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (14, {'rating': 1650, 'colorNum': 2, 'school': 'B', 'score': 3.0, 'label': 'Player14', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    # Score 3.5
    (15, {'rating': 1700, 'colorNum': 0, 'school': 'A', 'score': 3.5, 'label': 'Player15', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (16, {'rating': 1750, 'colorNum': 0, 'school': 'B', 'score': 3.5, 'label': 'Player16', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (17, {'rating': 1800, 'colorNum': 0, 'school': 'C', 'score': 3.5, 'label': 'Player17', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (18, {'rating': 1850, 'colorNum': 0, 'school': 'C', 'score': 3.5, 'label': 'Player18', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
    (19, {'rating': 1900, 'colorNum': 0, 'school': 'A', 'score': 3.5, 'label': 'Player19', 'matchHistory': [], 'color': 'White', 'colorStreak': 0}),
    (20, {'rating': 1950, 'colorNum': 0, 'school': 'B', 'score': 3.5, 'label': 'Player20', 'matchHistory': [], 'color': 'Black', 'colorStreak': 0}),
]

G.add_nodes_from(players)

score_groups = {}

# Populate the score_groups dictionary
for node, data in G.nodes(data=True):
    score = data['score']
    if score not in score_groups:
        score_groups[score] = []
    score_groups[score].append(node)

# Example usage of optimize_score_groups function
updated_groups = plausible_groups(G, score_groups)
print(updated_groups)

upper_lower_groups = best_UL_outcome(G, updated_groups)
print(upper_lower_groups)

final_pairings = extract_final_solution(G, updated_groups, upper_lower_groups)
pairs = []
for group in final_pairings:
    for i in final_pairings[group]:
        pairs.append(i)
print(final_pairings)