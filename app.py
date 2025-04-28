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
app = dash.Dash(
    __name__,
    server=server,
    update_title=None,
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
                "margin": "10px",
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
                "margin": "50px",
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

    if light_vector == graph.light_vector:
        app.layout['data-store'].data['update'] = False
    else:
        graph.on_update(light_vector, sensors)
        app.layout['data-store'].data['update'] = True
    return jsonify({"status": "success", "message": "Data received and processed"})


@app.callback([Output('3d-graph', 'figure'),Output('2d-graph', 'figure')],
              [Input('interval-component', 'n_intervals'),Input('data-store', 'data')])
def update_plot(n_intervals, data_store):
    print(data_store['update'])
    if not data_store['update']:
        #print("No update")
        raise PreventUpdate
    #print("Update")
    return graph.figure_3d, graph.figure_2d


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
