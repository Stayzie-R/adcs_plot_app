import os
import time
import queue
import flask
from flask import request, jsonify, Response

import dash
from dash import dcc, html, Output, Input,State
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
        dcc.Store(id='camera-store'),
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

@app.server.route('/update_vector', methods=['POST'])
def update_vector():
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
    return jsonify({"status": "success", "message": "Data received and processed"})


@app.callback([Output('3d-graph', 'figure'),
               Output('2d-graph', 'figure'),
               Output('camera-store', 'data')],
              [Input('interval-component', 'n_intervals')],
              [State('3d-graph', 'relayoutData')])
def update_plot(n_intervals, relayout_data):
    if relayout_data is None:
        camera_state = {}
    else:
        camera_state = relayout_data.get('scene', {}).get('camera', {})

    print("updating vector: ", str(graph.light_vector))

    figure_3d = graph.figure_3d
    figure_2d = graph.figure_2d
    if camera_state:
        figure_3d['layout']['scene']['camera'] = camera_state

    return figure_3d, figure_2d, camera_state


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
