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
        # Store pro uložení hodnoty light_vector
        dcc.Store(id='light-vector-store', data={}),
        html.Div(id='light-vector-output')  # Zobrazování nové hodnoty light_vector
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

    print("Data received")
    # Vrátíme nový vektor do dcc.Store přes Dash callback
    app.client_data['light-vector-store.data'] = light_vector
    return flask.Response("Vector updated", status=200)

# Callback pro zobrazení hodnoty light_vector
@app.callback(
    Output('light-vector-store', 'data'),
    Input('light-vector-store', 'data'),
    prevent_initial_call=True
)
def store_light_vector(light_vector):
    # Nastavíme novou hodnotu pro light_vector
    if not light_vector:
        raise PreventUpdate
    return light_vector

# Callback pro zobrazení hodnoty light_vector
@app.callback(
    Output('light-vector-output', 'children'),
    Input('light-vector-store', 'data')  
)
def update_output(light_vector):
    if not light_vector:
        raise PreventUpdate  
    return f'Nová hodnota light_vector: {light_vector}'

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
