import os
import time
import queue
import flask
from flask import request, jsonify, Response

import dash
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate

import config
from graph import Graph


server = flask.Flask(__name__)
secret_key = os.environ.get("SECRET_KEY", "secret")
app = dash.Dash(
    __name__,
    server=server,
    update_title="", #NONE
    suppress_callback_exceptions=True
)

graph = Graph()

app.title = "ADCS - Visualization"
app.update_title=None
app.layout = html.Div(
    children=[
        dcc.Graph(
            id="3d-graph",
            figure=graph.figure_3d,
            style={
                "margin": "0px",
                "display": "inline-block",

            },
            config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d']
            }
        ),
        dcc.Graph(
            id="2d-graph",
            figure=graph.figure_2d,
            style={
                "margin": "0px",
                "display": "inline-block",
            },
            config={
                'modeBarButtonsToRemove': ['zoom3d', 'pan3d', 'select3d', 'lasso3d', 'resetCameraLastSave3d', 'resetCameraDefault3d']
            }
        ),
        dcc.Interval(id='interval-component',interval=1000),
        dcc.Store(id='data-store', data={'update': False})
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh",
        "gap": "10px"
    }
)




if __name__ == "__main__":
    app.run(debug=config.DEBUG,use_reloader=False)
