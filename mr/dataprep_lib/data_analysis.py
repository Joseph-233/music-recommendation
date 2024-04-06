import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(filepath)

def plot_correlation_matrix(df):
    """Plot a correlation matrix for the DataFrame."""
    plt.figure(figsize=(10, 8))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.show()

def main_analysis(filepath):
    """Load data and perform a series of analysis functions."""
    df = load_data(filepath)
    print("Data loaded successfully.")
    plot_correlation_matrix(df)
