import os
import flask
from flask import request, jsonify

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
    update_title="ADCS",
    suppress_callback_exceptions=True
)

graph = Graph()

app.layout = html.Div(
    children=[
        dcc.Graph(
            id="3d-graph",
            figure=graph.figure,
            style={
                "margin": "auto",
                "display": "block"
            },
            config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d']
            }
        ),
        dcc.Store(id="light-vector-store"),
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh"
    }
)

@app.server.route('/update_vector', methods=['POST'])
def update_vector():
    data = request.get_json()

    light_vector = data["light_vector"]
    sensors = [
        {
            "color": sensor["color"],
            "vector": sensor["vector"],
            "value": round(sensor["value"], 4)
        }
        for sensor in data["sensors"]
    ]
    graph.on_update(light_vector, sensors)

    def event_stream():
        yield f"data: Vector updated\n\n"
        time.sleep(1)  

    return Response(event_stream(), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
