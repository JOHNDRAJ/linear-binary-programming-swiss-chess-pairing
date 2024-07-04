import matplotlib.pyplot as plt

def plot_dict(data):
    """
    Plot a dictionary where keys are integers and values are lists of floats.
    
    Args:
        data (dict): The dictionary to plot. Keys should be integers and values should be lists of floats.
    """
    # Create a figure and an axis
    fig, ax = plt.subplots()

    # Plot each list of values for their respective key
    for key, values in data.items():
        x_values = [key] * len(values)  # Create a list of x values that are all the same key
        ax.plot(x_values, values, 'o')  # 'o' indicates circular markers

    # Set labels and title
    ax.set_xlabel('Keys')
    ax.set_ylabel('Values')
    ax.set_title('Visual Representation of Dictionary Data')

    # Show the plot
    plt.show()