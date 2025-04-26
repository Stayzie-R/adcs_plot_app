import os
import flask
from flask import request
from flask_socketio import SocketIO, emit

import dash
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate

import config
from graph import Graph

# Nastavení Flask serveru a Flask-SocketIO
server = flask.Flask(__name__)
secret_key = os.environ.get("SECRET_KEY", "secret")
socketio = SocketIO(server)

app = dash.Dash(
    __name__,
    server=server,
    update_title="ADCS"
)

graph = Graph()

# Layout aplikace
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
        dcc.Store(id='graph_update_store'),
        html.Pre(id='camera-output')
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh"
    }
)


# Callback pro sledování pozice kamery
@app.callback(
    Output('camera-output', 'children'),
    Input('3d-graph', 'relayoutData')
)
def update_camera(relayout_data):
    if relayout_data and 'scene.camera' in relayout_data:
        camera = relayout_data['scene.camera']['eye']
    #     return f"Camera position:\nx: {camera['x']:.2f}, y: {camera['y']:.2f}, z: {camera['z']:.2f}"
    # return "Camera position: not moved yet"


# Endpoint pro aktualizaci vektorů
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

    # for sensor in sensors:
    #     print("__________SENSOR_________")
    #     print("received sensor data")
    #     print("color:", sensor["color"], ", type:", type(sensor["color"]))
    #     print("vector:", sensor["vector"], ", type:", type(sensor["vector"]))
    #     print("_________________________")

    graph.on_update(light_vector, sensors)

    socketio.emit('graph_update', {
        'light_vector': light_vector,
        'sensors': sensors
    })
    return flask.Response("Vector updated", status=200)


@app.callback(
    Output("3d-graph", "figure"),
    Input('graph_update_store', 'data'),
    prevent_initial_call=True
)
def update_graph(data):
    print("HERE HERE HERE")
    if data is None:
        raise PreventUpdate
    return data


if __name__ == "__main__":
    socketio.run(
        app.server,
        debug=config.DEBUG,
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000)),
        #port=8050,
        #allow_unsafe_werkzeug=True
    )