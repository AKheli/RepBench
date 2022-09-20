# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
import sys

import dash
from dash import Dash, html, dcc, Output, Input
import plotly.express as px
from pandas import DataFrame

from data_methods.data_class import DataContainer

app = Dash(__name__)
server = app.server

df: DataFrame = DataContainer("bafu").original_data
df_norm: DataFrame = DataContainer("bafu").norm_data

fig = px.scatter(data_frame=df, x=df.index, y=df.columns.values, title="df")
fig2 = px.scatter(data_frame=df_norm, x=df.index, y=df_norm.columns.values, title="normalized df")

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''Dash: A web application framework for your data.'''),
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        dcc.Graph(
            id='example-graph2',
            figure=fig2
        ),

    ], style={'overflowY': 'scroll', 'height': 500}),
    html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''Dash: A web application framework for your data.'''),
        dcc.Graph(
            id='example-graph5',
            figure=fig
        ),
        dcc.Graph(
            id='example-graph3',
            figure=fig2
        ),

    ], style={'overflowY': 'scroll', 'height': 500})
    , html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='normal', type='text')
    ])
])

@app.callback(
    Output(component_id='example-graph5', component_property='figure'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    print(input_value)
    if input_value == "stand":
        return fig2
    return fig




from os.path import dirname

if __name__ == '__main__':
    os.chdir(dirname(__file__))
    app.run_server(debug=True)
