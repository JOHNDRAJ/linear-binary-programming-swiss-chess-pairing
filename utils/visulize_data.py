import pandas as pd
import matplotlib.pyplot as plt

def visualize_scores(csv_file_path):
    # Read CSV data
    df = pd.read_csv(csv_file_path)

    # Create a DataFrame with the players and their scores
    players = pd.concat([df[['Node1', 'Node1 Label', 'Node1 Score']], 
                         df[['Node2', 'Node2 Label', 'Node2 Score']].rename(columns={'Node2': 'Node1', 'Node2 Label': 'Node1 Label', 'Node2 Score': 'Node1 Score'})])

    # Rename columns for clarity
    players.columns = ['Node', 'Label', 'Score']

    # Drop duplicates to ensure each player is listed once
    players = players.drop_duplicates(subset=['Label'])

    # Sort by score
    players = players.sort_values(by='Score', ascending=False)

    # Merge to get opponent information
    df1 = df[['Node1', 'Node1 Label', 'Node1 Score', 'Node2 Label', 'Result']]
    df2 = df[['Node2', 'Node2 Label', 'Node2 Score', 'Node1 Label', 'Result']]
    df2.columns = ['Node1', 'Node1 Label', 'Node1 Score', 'Node2 Label', 'Result']

    # Concatenate and remove duplicates
    merged = pd.concat([df1, df2]).drop_duplicates(subset=['Node1 Label'])

    # Merge to get a complete DataFrame with opponent information
    complete = pd.merge(players, merged, left_on='Label', right_on='Node1 Label', how='left')

    # Drop unnecessary columns
    complete = complete[['Node1 Label', 'Score','Node2 Label', 'Result']]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    table = ax.table(cellText=complete.values, colLabels=complete.columns, cellLoc='center', loc='center')

    # Adjust layout
    table.scale(1, 2)
    plt.title('Players Sorted by Score with Opponent Information')
    plt.show()
