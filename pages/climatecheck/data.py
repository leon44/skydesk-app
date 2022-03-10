"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_dataframe_tmax():
    """Create Pandas DataFrame from local file."""
    df = pd.read_feather('data/ghcnd-tmax.feather')
    return df
