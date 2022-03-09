"""Instantiate a Dash app."""
import dash
from dash import dcc
from dash import html
from dash import dash_table
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

    # Create Layout
    s=60
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name='name',
                        hover_data=['id'],
                        #color='Latitude',
                        zoom=0, height=20*s
                        #width=16*s
                        #range_color=[-90,90],
                        #color_discrete_sequence=["green", "blue", "goldenrod", "magenta"]
                       )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="histogram-graph",
                figure=fig),
            #create_data_table(df),
        ],
        id="dash-container",
    )
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
