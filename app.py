import os
import flask
from flask import request

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
        dcc.Store(id='light-vector-store', data=update_light_vector()),
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh"
    }
)

light_vector = np.random.rand(3).tolist()

@app.server.route('/update_vector', methods=['POST'])
def update_vector():
    global light_vector
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

    print("Emitting graph_update with data:", {
        'light_vector': light_vector,
        'sensors': sensors
    })

    return flask.Response("Vector updated", status=200)

@app.callback(
    Output('light-vector-output', 'children'),
    Input('light-vector-store', 'data')
)
def update_output(light_vector):
    print("Callback1")
    return f'Nová hodnota light_vector: {light_vector}'


@app.callback(
    Output('light-vector-store', 'data'), Input('light-vector-store', 'data'),
    prevent_initial_call=True
)
def update_store(light_vector):
    print("Callback2")
    return light_vector


@app.callback(
    Output('light-vector-store', 'data'),
    Input('light-vector-store', 'data'),
    prevent_initial_call=True
)
def update_store(light_vector):
    if dash.callback_context.triggered:
        print("Callback3!")
    return light_vector


@app.callback(
    Output('light-vector-store', 'data'),Input('light-vector-store', 'data'),prevent_initial_call=True
)
def update_store(light_vector):
    print("callback4")
    return light_vector

if __name__ == "__main__":
    app.run(debug=config.DEBUG)