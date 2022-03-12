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

from .data import create_df_tmax
from .data import create_df_station
from .data import create_heat_map
from .data import create_map
from .layout import html_layout
import plotly.express as px

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/climatecheck/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Load DataFrame
    df = create_df_tmax()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            selector(),
            heat_map_container(),
            #line_chart_container(),
            dcc.Graph(
                id="map",
                figure=create_map(df)),
            ],
            id="dash-container",
    )

    @dash_app.callback(
        Output('selection-info', 'children'),
        Input('map', 'clickData'))
    def display_click_data(clickData):
        if clickData == None:
            txt = 'Select a point on the map to get started'
        else:
            statName = clickData['points'][0]['hovertext']
            statID = clickData['points'][0]['customdata'][0]
            dataUrl = f'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{statID}.csv'
            txt = html.Div(children=[
                f'You have selected {statName}, {statID} ',
                    dcc.Link('Raw data', href=dataUrl, target="_blank")])
        return txt

    @dash_app.callback(
        dash.dependencies.Output('run-button', 'children'),
        [dash.dependencies.Input('map', 'clickData')])
        #[dash.dependencies.State('click-data', 'value')])
    def update_output(clickData):
        txt = ''
        if clickData is not None:
            statName = clickData['points'][0]['hovertext']
            txt = html.Div(children=[
                html.Button(f'Run analysis for {statName}', id='run-anal')]),
        return txt

    @dash_app.callback(
        dash.dependencies.Output('heat-map', 'figure'),
        [dash.dependencies.Input('run-anal', 'n_clicks'),
         dash.dependencies.Input('map', 'clickData')])
    def update_output(n_clicks, clickData):
        heatmap = 'soon'
        if n_clicks is not None:
            statID = clickData['points'][0]['customdata'][0]
            txt = f'now running for {statID}'
            dfFull, use = create_df_station(statID)
            heatmap = create_heat_map(dfFull, use)
            #txt = f'{df.max()}'
        return heatmap

    return dash_app.server

def selector():
    sel = html.Div([
        html.Pre(id='selection-info'),
        html.Pre(id='run-button'),
        html.Div(html.P([html.Br()]))
    ])
    return sel

def heat_map_container():
    hmc = html.Div([
        html.Pre(dcc.Loading(id='loading-1', type='default',
                             children=html.Div(dcc.Graph(
                                 id="heat-map",
                                 figure="heat-map"))))
             ])
    return hmc

def line_chart_container():
    lcc = html.Div([
        html.Pre(dcc.Loading(id='loading-2', type='default',
                             children=html.Div(dcc.Graph(
                                 id="line-chart",
                                 figure="line-chart"))))
             ])
    return lcc