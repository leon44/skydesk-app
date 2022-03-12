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
            selector(),
            dcc.Graph(
                id="map",
                figure=fig),
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
        fig = 'soon'
        if n_clicks is not None:
            statID = clickData['points'][0]['customdata'][0]
            txt = f'now running for {statID}'
            dfFull = create_df_station(statID)
            fig = heatMap(dfFull)
            #txt = f'{df.max()}'
        return fig

    return dash_app.server

def selector():
    sel = html.Div([
        html.Pre(id='selection-info'),
        html.Pre(id='run-button'),
        html.Pre(dcc.Loading(id='loading-1', type='default', children=html.Div(dcc.Graph(
                id="heat-map",
                figure="heat-map"))),
                             ),
        html.Div(html.P([html.Br()]))
    ])
    return sel

def heatMap(dfFull):
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
    fig = px.imshow(dfH, text_auto='.1f',
                    labels=dict(x="Year", y="Month", color="Average Temp"),
                    y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                    # x=list(range(1980,2020))
                    )
    fig = fig.show()
    return fig