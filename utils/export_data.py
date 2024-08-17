# # import networkx as nx
# # import csv

# # def calculate_score(G, node):
# #     """Calculate the score of a node as the sum of the weighted outgoing edges minus the total number of outgoing edges."""
# #     total_weight = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
# #     num_outgoing_edges = G.out_degree(node)
# #     score = total_weight - num_outgoing_edges
# #     return score

# # def export_node_pair_info_to_csv(G, node_pairs, filename):
# #     """Export node pair information to a CSV file."""
# #     with open(filename, mode='w', newline='') as file:
# #         writer = csv.writer(file)
# #         # Write header
# #         writer.writerow(['Node1', 'Node1 Label', 'Node1 Color', 'Node1 Score', 'Node2', 'Node2 Label', 'Node2 Color', 'Node2 Score', 'Result'])

# #         for node1, node2 in node_pairs:
# #             node1_label = f"{G.nodes[node1]['label']}: {str(G.nodes[node1]['rating'])}"
# #             node1_color = G.nodes[node1]['color']
# #             node1_score = calculate_score(G, node1)
# #             node2_label = f"{G.nodes[node2]['label']}: {str(G.nodes[node2]['rating'])}"
# #             node2_color = G.nodes[node2]['color']
# #             node2_score = calculate_score(G, node2)
            
# #             # Determine the result based on the edge weight
# #             if G[node1][node2]['weight'] == 2:
# #                 result = 'win'
# #             elif G[node1][node2]['weight'] == 1.5:
# #                 result = 'draw'
# #             elif G[node1][node2]['weight'] == 1:
# #                 result = 'loss'
# #             else:
# #                 result = 'unknown'  # Handle unexpected weights

# #             # Write row for each pair
# #             writer.writerow([node1, node1_label, node1_color, node1_score, node2, node2_label, node2_color, node2_score, result])


# import networkx as nx
# import csv

# def calculate_score(G, node):
#     """Calculate the score of a node as the sum of the weighted outgoing edges minus the total number of outgoing edges."""
#     total_weight = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
#     num_outgoing_edges = G.out_degree(node)
#     score = total_weight - num_outgoing_edges
#     return score

# def export_node_pair_info_to_csv(G, node_pairs, filename):
#     """Export node pair information to a CSV file."""
#     with open(filename, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         # Write header
#         writer.writerow(['Node1 School', 'Node1 Label', 'Node1 Color', 'Node1 Score', 'Node2 School', 'Node2 Label', 'Node2 Color', 'Node2 Score', 'Result'])

#         for node1, node2 in node_pairs:
#             node1_school = G.nodes[node1]['school']
#             node1_label = f"{G.nodes[node1]['label']}: {str(G.nodes[node1]['rating'])}"
#             node1_color = G.nodes[node1]['color']
#             node1_score = calculate_score(G, node1)
#             node2_school = G.nodes[node2]['school']
#             node2_label = f"{G.nodes[node2]['label']}: {str(G.nodes[node2]['rating'])}"
#             node2_color = G.nodes[node2]['color']
#             node2_score = calculate_score(G, node2)
            
#             # Determine the result based on the edge weight
#             if G[node1][node2]['weight'] == 2:
#                 result = 'win'
#             elif G[node1][node2]['weight'] == 1.5:
#                 result = 'draw'
#             elif G[node1][node2]['weight'] == 1:
#                 result = 'loss'
#             else:
#                 result = 'unknown'  # Handle unexpected weights

#             # Write row for each pair
#             writer.writerow([node1_school, node1_label, node1_color, node1_score, node2_school, node2_label, node2_color, node2_score, result])


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
        writer.writerow(['Node1 Label', 'Node1 School', 'Node1 Color', 'Node1 Score', 'Node2 Label', 'Node2 School', 'Node2 Color', 'Node2 Score', 'Result'])

        for node1, node2 in node_pairs:
            if node1 == 'BYE':
                # For Node1 is BYE, fill with 'BYE' and get Node2 info
                node1_school = 'BYE'
                node1_label = 'BYE'
                node1_color = 'BYE'
                node1_score = 'BYE'
                node2_school = G.nodes[node2]['school']
                node2_label = f"{G.nodes[node2]['label']}: {str(G.nodes[node2]['rating'])}"
                node2_color = G.nodes[node2]['color']
                node2_score = calculate_score(G, node2)
            elif node2 == 'BYE':
                # For Node2 is BYE, fill with 'BYE' and get Node1 info
                node1_school = G.nodes[node1]['school']
                node1_label = f"{G.nodes[node1]['label']}: {str(G.nodes[node1]['rating'])}"
                node1_color = G.nodes[node1]['color']
                node1_score = calculate_score(G, node1)
                node2_school = 'BYE'
                node2_label = 'BYE'
                node2_color = 'BYE'
                node2_score = 'BYE'
            else:
                # For regular nodes, extract and calculate information
                node1_school = G.nodes[node1]['school']
                node1_label = f"{G.nodes[node1]['label']}: {str(G.nodes[node1]['rating'])}"
                node1_color = G.nodes[node1]['color']
                node1_score = calculate_score(G, node1)
                node2_school = G.nodes[node2]['school']
                node2_label = f"{G.nodes[node2]['label']}: {str(G.nodes[node2]['rating'])}"
                node2_color = G.nodes[node2]['color']
                node2_score = calculate_score(G, node2)

            # Determine the result based on the edge weight, if both nodes are not 'BYE'
            if node1 != 'BYE' and node2 != 'BYE':
                if G[node1][node2]['weight'] == 2:
                    result = 'win'
                elif G[node1][node2]['weight'] == 1.5:
                    result = 'draw'
                elif G[node1][node2]['weight'] == 1:
                    result = 'loss'
                else:
                    result = 'unknown'  # Handle unexpected weights
            else:
                result = 'N/A'  # No result if one of the nodes is 'BYE'

            # Write row for each pair
            writer.writerow([node1_label, node1_school, node1_color, node1_score, node2_label, node2_school, node2_color, node2_score, result])


