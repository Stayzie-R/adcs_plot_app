
import os

import dash
from dash import dcc, html, Output, Input
from TestGraph import TestGraph
import flask
from flask import request, jsonify, Response
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)

server = flask.Flask(__name__)
secret_key = os.environ.get("SECRET_KEY", "secret")
app = dash.Dash(
    __name__,
    server=server,
    update_title="",
)
graph = TestGraph()

app.title = "ADCS - Visualization"
app.layout = html.Div(
    children=[
        dcc.Graph(
            id="graph",
            figure=graph.fig,
        ),
        dcc.Interval(id='interval-component',interval=1000),
    ],
)

@app.server.route('/test', methods=['POST'])
def update_vector():
    data = request.get_json()
    light_vector = data["light_vector"]
    graph.update_vector(light_vector)
    print("received vector: ", str(graph.light_vector))
    return jsonify({"status": "success", "message": "Data received and processed"})


@app.callback(Output('graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_plot(n_intervals):
    print("updating vector: ", str(graph.light_vector))
    return graph.fig


if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
