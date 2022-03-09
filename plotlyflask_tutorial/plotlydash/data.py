"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_dataframe():
    """Create Pandas DataFrame from local file."""
    headings = ['id', 'lat', 'lon', 'ele','0','name','type','wmo']
    df = pd.read_fwf('data/ghcnd-stations.txt', names=headings, infer_nrows=26000)
    return df
