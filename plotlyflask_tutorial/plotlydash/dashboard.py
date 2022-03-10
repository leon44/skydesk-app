"""Instantiate a Dash app."""
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input
from dash import Output
#import json
import numpy as np
import pandas as pd

from .data import create_dataframe
from .layout import html_layout
import plotly.express as px

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Load DataFrame
    df = create_dataframe()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Generate figure
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name='name',
                        hover_data=['id', 'start', 'end'],
                        zoom=3, height=20*60,
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

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            selector(df),
            dcc.Graph(
                id="map",
                figure=fig),
            ],
            id="dash-container",
    )

    @dash_app.callback(
        Output('click-data', 'children'),
        Input('map', 'clickData'))
    def display_click_data(clickData):
        if clickData == None:
            txt = 'Select a point on the map to get started'
        else:
            statName = clickData['points'][0]['hovertext']
            statID = clickData['points'][0]['customdata'][0]
            dataUrl = f'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{statID}.csv'
            txt = html.Div(children=[
                f'you have selected {statName}, {statID} ',
                    dcc.Link('Download raw data', href=dataUrl, target="_blank")])
        return txt

    return dash_app.server

def selector(df):
    sel = html.Div([
        html.Pre(id='click-data'),
    ])
    return sel
