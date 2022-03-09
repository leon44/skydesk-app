"""Instantiate a Dash app."""
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import Input
from dash import Output
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
                        hover_data=['id'],
                        zoom=0, height=20*60,
                        color_discrete_sequence=["green", "blue", "goldenrod", "magenta"]
                       )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # Create Layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure=fig),
            #create_data_table(df),
            input_box(df),
            ],
            id="dash-container",
    )

    @dash_app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value')
    )
    def update_output_div(input_value):
        output_value = float(input_value)+5.0
        return f'Output: {output_value}'

    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="database-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    return table

def input_box(df):
    box = html.Div([
        html.H6("Change the value in the text box to add 5 to it!"),
        html.Div([
            "Input: ",
            dcc.Input(id='my-input', value='25', type='text')
        ]),
        html.Br(),
        html.Div(id='my-output'),
    ])
    return box
