import os
import time
from datetime import datetime, timedelta, timezone

import flask
from flask import request, jsonify, Response


import dash
from dash import dcc, html, Output, Input, State, no_update
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

with open("camera_interaction.html", "r") as f:
    app.index_string = f.read()


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
                "padding": "0px"
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
                "padding": "0px",
                "margin-left": "0px"
            },
            config={
                'modeBarButtonsToRemove': ['zoom3d', 'pan3d', 'select3d', 'lasso3d', 'resetCameraLastSave3d', 'resetCameraDefault3d']
            }
        ),
        dcc.Interval(id='interval-component',interval=1000),
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh",
        "gap": "10px"
    }
)

last_data_update_time = datetime.now(timezone.utc)
data_timeout = timedelta(seconds=5)
data_has_arrived = False

@app.server.route('/update_vector', methods=['POST'])
def update_vector():
    global last_data_update_time, data_has_arrived
    data = request.get_json()
    print("received vector: ", str(graph.light_vector))
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
    last_data_update_time = datetime.now(timezone.utc)
    data_has_arrived = True
    return jsonify({"status": "success", "message": "Data received and processed"})


camera_move_lock = False

@app.server.route('/interaction_start', methods=['POST'])
def lock_camera_backend():
    global camera_move_lock
    lock = True
    return jsonify(status="ok")


@app.server.route('/interaction_end', methods=['POST'])
def unlock_camera_backend():
    global camera_move_lock
    camera_move_lock = False
    print("Camera unlocked from frontend!")
    return jsonify(status="unlocked")


@app.callback(
    [Output('3d-graph', 'figure'), Output('2d-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_plot(n_intervals):
    global camera_move_lock, last_data_update_time, data_timeout, data_has_arrived
    if not data_has_arrived:
        return no_update, no_update
    if datetime.now(timezone.utc) - last_data_update_time > data_timeout:
        graph.on_remove()
        data_has_arrived = False
        last_data_update_time = now
    if camera_move_lock:
        return no_update, graph.figure_2d
    return graph.figure_3d, graph.figure_2d



if __name__ == "__main__":
    app.run(debug=config.DEBUG)
