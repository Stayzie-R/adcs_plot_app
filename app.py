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


    print("Data received")

    app.server.dash_clientside.set_props(
        "light-vector-store", {"data": light_vector}
    )
    return flask.Response("Vector updated", status=200)


# Callback pro aktualizaci grafu
@app.callback(
    Output('3d-graph', 'figure'),
    Input('light-vector-store', 'data')
)
def update_graph(light_vector):
    if light_vector is None:
        raise PreventUpdate  # Neprovádět změny, pokud není žádný nový light_vector
    print("Updating the graph with new vector")
    return graph.figure


# Callback pro aktualizaci light_vector ve store
@app.callback(
    Output('light-vector-store', 'data'),
    [Input('3d-graph', 'id')]
)
def update_light_vector_from_flask(n):
    print("new vector")
    if light_vector is not None:
        return light_vector
    raise PreventUpdate



if __name__ == "__main__":
    app.run(debug=config.DEBUG)
