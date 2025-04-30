import os
import time
from datetime import datetime, timedelta, timezone

import flask
from flask import request, jsonify, Response

import dash
from dash import dcc, html, Output, Input, State, no_update
from dash.exceptions import PreventUpdate

import config_app as config
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
        dcc.Interval(id='interval-component',interval=config.RELOAD_INTERVAL),
        html.Pre(id='camera-output')
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
data_has_arrived = False
data_timeout = timedelta(seconds=config.DATA_UPDATE_TIMEOUT_SECONDS)

@app.server.route('/update_vector', methods=['POST'])
def update_vector():
    global last_data_update_time, data_has_arrived
    data = request.get_json()
    print("[INFO] Received new vector update from client:", str(graph.light_vector))
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

# @app.callback(
#      Output('camera-output', 'children'), Input('3d-graph', 'relayoutData'))
# def update_camera(relayout_data):
#     if relayout_data and 'scene.camera' in relayout_data:
#          camera = relayout_data['scene.camera']['eye']
#          #return f"Camera position:\nx: {camera['x']:.2f}, y: {camera['y']:.2f}, z: {camera['z']:.2f}"
#     return "Camera position: not moved yet"


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
    global camera_move_lock, last_data_update_time, data_has_arrived, data_timeout

    # If no data has ever been received yet, do nothing (avoid clearing graph too early)
    if not data_has_arrived:
        print("[INFO] No data received yet — skipping graph update.")
        return no_update, no_update

    # Check if data hasn't been updated within the timeout period
    if datetime.now(timezone.utc) - last_data_update_time > data_timeout:
        print("[WARNING] No new data received, Data timeout reached — clearing graph.")
        graph.on_remove()                
        data_has_arrived = False         # Reset flag 

    # If the camera is currently being moved, avoid updating the 3D graph
    if camera_move_lock:
        print("[INFO] Camera movement in progress — skipping 3D graph update.")
        return no_update, graph.figure_2d

    # Normal case: update both graphs
    print("[INFO] Data is up-to-date — updating both graphs.")
    return graph.figure_3d, graph.figure_2d



if __name__ == "__main__":
    app.run(debug=config.DEBUG)
