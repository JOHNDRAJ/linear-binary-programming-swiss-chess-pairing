import networkx as nx
import random


def add_weighted_edges(G, node_pairs):
    # Define the weight options
    weight_options = [
        (2, 1),    # Option 1: weight (i,j) as 2 and (j,i) as 1
        (1.5, 1.5),# Option 2: weight (i,j) as 1.5 and (j,i) as 1.5
        (1, 2)     # Option 3: weight (i,j) as 1 and (j,i) as 2
    ]

    w = [[0.84, 0.09, 0.07], [0.79, 0.11, 0.1],[0.70, 0.13, 0.17], [0.60, 0.15, 0.25], [0.47, 0.17, 0.36], [0.42, 0.17, 0.42]]

    # Iterate over each node pair
    for i, j in node_pairs:
        # Randomly choose one of the weight options
        if (G.nodes[i]['rating'] - G.nodes[j]['rating']) > 400:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[0], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > 300:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[1], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > 200:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[2], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > 100:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[3], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > 0:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[4], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) == 0:
            weight_ij, weight_ji = random.choices(weight_options, weights=w[5], k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > -100:
            weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[4]), k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > -200:
            weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[3]), k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > -300:
            weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[2]), k=1)[0]
        elif (G.nodes[i]['rating'] - G.nodes[j]['rating']) > -400:
            weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[1]), k=1)[0]
        else:
            weight_ij, weight_ji = random.choices(weight_options, weights=reversed(w[0]), k=1)[0]

        if weight_ij == 2:
            G.nodes[i]['score'] += 1
        elif weight_ij == 1.5:
            G.nodes[i]['score'] += 0.5
            G.nodes[j]['score'] += 0.5
        else:
            G.nodes[j]['score'] += 1

        
        
        

        # Update the weights in the graph
        G.add_edge(i, j, weight=weight_ij)
        G.add_edge(j, i, weight=weight_ji)

    return G