# import pandas as pd
# import ast

# def transform_csv_data(csv_file_path):
#     # Read CSV data
#     df = pd.read_csv(csv_file_path)

#     # Convert string representations of lists to actual lists if needed (remove if 'color' is not a list)
#     # df['Node1_Color'] = df['Node1_Color'].apply(ast.literal_eval)
#     # df['Node2_Color'] = df['Node2_Color'].apply(ast.literal_eval)

#     # Create a new DataFrame with the desired format
#     transformed_data = pd.DataFrame({
#         'Node1': df['Node1'],
#         'Node1 Label': df['Node1 Label'],
#         'Node1 Color': df['Node1 Color'],
#         'Node1 Score': df['Node1 Score'],
#         'Node2': df['Node2'],
#         'Node2 Label': df['Node2 Label'],
#         'Node2 Color': df['Node2 Color'],
#         'Node2 Score': df['Node2 Score'],
#         'Result': df['Result']
#     })

#     return transformed_data

import pandas as pd
import ast

def transform_csv_data(csv_file_path):
    # Read CSV data
    df = pd.read_csv(csv_file_path)

    # Create a new DataFrame with the desired format
    transformed_data = pd.DataFrame({
        'Node1 Label': df['Node1 Label'],
        'Node1 School': df['Node1 School'],
        'Node1 Color': df['Node1 Color'],
        'Node1 Score': df['Node1 Score'],
        'Node2 Label': df['Node2 Label'],
        'Node2 School': df['Node2 School'],
        'Node2 Color': df['Node2 Color'],
        'Node2 Score': df['Node2 Score'],
        'Result': df['Result']
    })

    return transformed_data
