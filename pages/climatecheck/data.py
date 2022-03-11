"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_df_tmax():
    """Create Pandas DataFrame from local file."""
    df = pd.read_feather('data/ghcnd-tmax.feather')
    return df

def create_df_station(statID):
    df = pd.read_csv(f'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{statID}.csv')
    return df