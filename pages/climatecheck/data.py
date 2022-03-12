"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd


def create_df_tmax():
    """Create Pandas DataFrame from local file."""
    df = pd.read_feather('data/ghcnd-tmax.feather')
    return df

def create_df_station(statID):
    df = pd.read_csv(f'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{statID}.csv',
                     index_col=['DATE'], parse_dates=['DATE'])

    try:
        tavgCount = df.TAVG.count()
    except: tavgCount = 0

    try:
        tmaxCount = df.TMAX.count()
    except: tmaxCount = 0

    if df.TMAX.count() > df.TAVG.count():
        use = 'TMAX'
    else:
        use = 'TAVG'

    #To celcius
    dfFull = df[[use]]/10

    #all, for heatmap
    #dfFull = df[use]

    #only full years, for line graph
    #df = df.drop(df[df.index.year == 2022].index)

    return dfFull