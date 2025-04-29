import plotly.graph_objects as go

class TestGraph:
    def __init__(self):
        self.light_vector = [0.0, 0.0, 0.0]
        self.fig = go.Figure()
        self.light_vector_annotation = None  # uchováme odkaz
        self._setup_layout()
        self.print_graph()

    def _setup_layout(self):
        self.fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='white'
        )

    def print_graph(self):
        if self.light_vector_annotation is None:
            self.light_vector_annotation = dict(
                text=f"light_vector: {self.light_vector}",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16),
            )
            self.fig.add_annotation(self.light_vector_annotation)
        else:
            self.light_vector_annotation['text'] = f"light_vector: {self.light_vector}"
            self.fig.update_layout(annotations=[self.light_vector_annotation if a['text'].startswith("light_vector") else a for a in self.fig.layout.annotations])

    def update_vector(self, light_vector):
        self.light_vector = light_vector
        self.print_graph()
