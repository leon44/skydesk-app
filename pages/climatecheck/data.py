"""Prepare data for Plotly Dash."""
import numpy as np
import pandas as pd
import plotly.express as px

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

    if tmaxCount > tavgCount:
        use = 'TMAX'
    else:
        use = 'TAVG'

    #To celcius
    dfFull = df[[use]]/10

    return dfFull, use

def create_heat_map(dfFull, use, statName):
    dfH = dfFull.drop(dfFull[dfFull.index.year < 1980].index)
    dfH = dfH.resample('M').mean()
    # dfH = dfH.rolling(5).mean()
    dfH['year'] = dfH.index.year
    dfH['month'] = dfH.index.month
    dfH = dfH.set_index('month')
    dfH = dfH.set_index('year', append=True)
    dfH = dfH.stack().unstack(level=0)
    dfH = dfH.transpose()
    dfH.columns = dfH.columns.droplevel(1)
    fig = px.imshow(dfH, text_auto='.1f', title=f'Monthly average {use} at {statName}',
                    labels=dict(x="Year", y="Month", color=f'Average {use}'),
                    y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')

    return fig

def create_line_chart(dfFull, use, statName):
    dfG = dfFull.resample('Y').mean()
    dfRoll = dfG.rolling(5).mean()
    fig = px.line(dfRoll, y=use, title=f'Five year rolling average {use} at {statName}')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')
    #fig.show()
    return fig

def create_map(df):
    # Generate map for station selection
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name='name',
                        hover_data=['id', 'start', 'end'],
                        zoom=3, #height=100%, #height=20*60,
                        color_discrete_sequence=["orange", "blue", "goldenrod", "magenta"]
                       )
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
