import networkx as nx
import csv

def calculate_score(G, node):
    """Calculate the score of a node as the sum of the weighted outgoing edges minus the total number of outgoing edges."""
    total_weight = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
    num_outgoing_edges = G.out_degree(node)
    score = total_weight - num_outgoing_edges
    return score

def export_node_pair_info_to_csv(G, node_pairs, filename):
    """Export node pair information to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Node1', 'Node1 Label', 'Node1 Score', 'Node2', 'Node2 Label', 'Node2 Score'])

        for node1, node2 in node_pairs:
            node1_label = G.nodes[node1]['label']
            node1_score = calculate_score(G, node1)
            node2_label = G.nodes[node2]['label']
            node2_score = calculate_score(G, node2)
            
            # Write row for each pair
            writer.writerow([node1, node1_label, node1_score, node2, node2_label, node2_score])