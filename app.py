import os
import flask
from flask import request
from flask_socketio import SocketIO, emit

import dash
from dash import dcc, html, Output, Input
from dash.exceptions import PreventUpdate

import config
from graph import Graph


server = flask.Flask(__name__)
server = app.server
secret_key = os.environ.get("SECRET_KEY", "secret")
socketio = SocketIO(server, cors_allowed_origins="*", async_mode="eventlet")

app = dash.Dash(
    __name__,
    server=server,
    update_title="ADCS",
    suppress_callback_exceptions=True
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
        <script src="/socketio_client.js"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

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


@app.server.route('/update_vector', methods=['POST'])
def update_vector():
    data = request.get_json()
    print("Received update_vector data:", data)

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
    })  # Logování před odesláním dat na klienta

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