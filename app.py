import os
import time
import queue
import flask
from flask import request, jsonify,Response

import dash
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate

import config
from graph import Graph

server = flask.Flask(__name__)
secret_key = os.environ.get("SECRET_KEY", "secret")
message_queue = queue.Queue()
data_ready = False
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
        dcc.Interval(id='interval-component',interval=1000),
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
    global data_ready
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

    message_queue.put('new_data')
    graph.on_update(light_vector, sensors)
    data_ready = True
    return jsonify({"status": "success", "message": "Data received and processed"})

@app.callback(Output("3d-graph", "figure"),Input("interval-check", "n_intervals"),prevent_initial_call=True)
def check_for_update(n_intervals):
    global data_ready
    if data_ready:
        data_ready = False
        print(f"[Interval {n_intervals}] Nová data! Překresluji graf.")
        return graph.figure  # Vracíš už aktualizovaný graf
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
