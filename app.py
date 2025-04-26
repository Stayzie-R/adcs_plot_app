import os

import flask
from flask import request

import dash
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate
from dash_extensions import EventListener

import config
from graph import Graph


server = flask.Flask(__name__)
secret_key = os.environ.get("SECRET_KEY", "secret")

app = dash.Dash(
    __name__,
    server=server,
    update_title="ADCS"
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
        EventListener(
                    id="listener",
                    events=[{"event": "update_vector", "props": ["detail"]}],
                    logging=False,
                    children=[],
                ),
        html.Pre(id='camera-output')
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh"
    }
)

@app.callback(
    Output('camera-output', 'children'), Input('3d-graph', 'relayoutData'))
def update_camera(relayout_data):
    if relayout_data and 'scene.camera' in relayout_data:
        camera = relayout_data['scene.camera']['eye']
        #return f"Camera position:\nx: {camera['x']:.2f}, y: {camera['y']:.2f}, z: {camera['z']:.2f}"
    #return "Camera position: not moved yet"

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
    #     print("color:",sensor["color"], ",type:" ,type(sensor["color"]))
    #     print("vector:",sensor["vector"], ",type:" ,type(sensor["vector"]))
    #     print("_________________________")
        
    graph.on_update(light_vector, sensors)

    return flask.Response(f"""
                <script>
                window.dispatchEvent(new CustomEvent("update_vector", {{
                    detail: {{
                        light_vector: {light_vector}
                    }}
                }}));
                </script>
                """, mimetype='text/html')

@app.callback(Output("3d-graph", "figure"),Input("listener", "event"),prevent_initial_call=True)
def update_graph_on_event(e):
    print("")
    print("__here__")
    print("")
    return graph.figure

if __name__ == "__main__":
    app.run(debug=config.DEBUG)

