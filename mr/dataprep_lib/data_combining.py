import pandas as pd

def load_and_combine_data(file_paths):
    """Load multiple CSV files and combine them into a single DataFrame."""
    data_frames = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        data_frames.append(df)
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df

def clean_combined_data(df):
    """Perform cleaning operations on the combined DataFrame."""
    # Example: Drop columns with too many missing values
    df.dropna(axis=1, thresh=int(0.8 * len(df)), inplace=True)
    return df

def save_data(df, output_path):
    """Save the DataFrame to a CSV file."""
    df.to_csv(output_path, index=False)
