"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_dataframe():
    """Create Pandas DataFrame from local file."""
    df = pd.read_feather('ghcnd-stations.feather')
    return df
