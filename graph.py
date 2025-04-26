from itertools import combinations, product

import plotly.graph_objs as go
import numpy as np

import config

class Graph:
    """
    Class to create and manage a 3D scatter plot figure.
    """
    def __init__(self):
        """
        Initialize the Graph object with a configured figure.
        """
        self._config = config

        self.light_vector = [0.0, 0.0, 0.0]

        self.sensors = [
            {
                "color": color,
                "vector": vector,
                "value": 0.0
            }
            for color, vector in self._config.SENSORS.items()
        ]

        self._fig = go.Figure()
        self._configure_graph()
        self._plot_static_object()

    def _configure_graph(self):
        """
        Set up the graph's properties
        """
        self._fig.update_layout(
            title="ADCS",
            uirevision='constant',  # Keeps the layout intact when the data is updated
            dragmode='turntable',
            xaxis=dict(
                range=[0, 10],      # Range of the X axis
                fixedrange=True     # Disables zooming on the X axis
            ),
            yaxis=dict(
                range=[0, 10],      # Range of the Y axis
                fixedrange=True     # Disables zooming on the Y axis
            ),
            scene=dict(
                xaxis=dict(visible=False),       # Hides the X axis in the 3D scene
                yaxis=dict(visible=False),       # Hides the Y axis in the 3D scene
                zaxis=dict(visible=False),       # Hides the Z axis in the 3D scene
                camera=dict(                     # Defines the initial position of the camera.
                    eye=dict(x=1.8, y=1.1, z=1.14)
                )
            ),
            width=500,                           # Width of the graph in pixels
            height=500,                          # Height of the graph in pixels
            margin=dict(l=0, r=0, t=50, b=0),    # Margins around the graph
            legend=dict(
                x=1,  # Position to the right (x=1)
                y=0,  # Position at the bottom (y=0)
                traceorder='normal',  # The order of legend items based on their addition
                font=dict(size=10, color='#000'),
                title=dict(
                    text="Sensor values",  # Title of the legend
                    font=dict(size=12, color="black"),
                    side="top"  # Position of the title
                ),
                itemclick=False,
                itemdoubleclick=False,

            ),
            hovermode=False,
        )

    def _plot_static_object(self):
        """
        Plots all static elements of the 3D scene, including the box, base plane,
        sensor direction arrows, sensor ellipses, and the legend.

        This method is typically called once during initialization or when the
        scene needs to be redrawn with static components that do not change dynamically.
        """
        self._create_box()
        self._create_plane()
        self._create_sensors_arrow()
        self._create_sensors_ellipse()
        self._create_legend()

    def _create_box(self):
        """
        Adds a static 3D box outline to the figure.

        This method computes and plots the edges of a cube defined by the
        radius values in all three dimensions. It is intended for internal
        use to visualize static reference geometry within the 3D scene.
        The box's appearance is controlled by configuration parameters in
        config.py.
        """
        radius = [-self._config.BOX_SIZE, self._config.BOX_SIZE]
        for s, e in combinations(np.array(list(product(radius, radius, radius))), 2):
            if np.sum(np.abs(s - e)) == radius[1] - radius[0]:
                pos = [list(pair) for pair in zip(s, e)]
                self._fig.add_trace(
                    go.Scatter3d(
                        x=pos[0], y=pos[1], z=pos[2],
                        mode='lines',
                        line=dict(color=self._config.BOX_COLOR,
                                  width=self._config.BOX_LINEWIDTH,
                                  dash=self._config.BOX_LINESTYLE),
                        showlegend=False,
                        hoverinfo='none'
                    )
                ),

    def _create_plane(self):
        """
        Adds a semi-transparent horizontal plane to the 3D figure.

        This method generates a flat surface positioned at a fixed Z-level,
        used to represent a reference plane within the 3D scene.
        The plane's visibility and appearance are controlled by configuration
        parameters in config.py.
        """
        if self._config.ALLOW_PLANE:
            radius = [-self._config.BOX_SIZE, self._config.BOX_SIZE]
            x_values = self._config.PLANE_SCALE_FACTOR * np.linspace(radius, radius, 1)
            y_values = self._config.PLANE_SCALE_FACTOR * np.linspace(radius, radius, 1)
            x_mesh, y_mesh = np.meshgrid(x_values, y_values)
            z_mesh = np.ones_like(x_mesh) * -self._config.BOX_SIZE
            self._fig.add_trace(
                go.Surface(
                    x=x_mesh, y=y_mesh, z=z_mesh,
                    colorscale=[self._config.PLANE_COLOR] * len(x_mesh.flatten()),
                    showscale=False,
                    opacity=.1,
                    hoverinfo='none',
                    contours=dict(
                        x=dict(show=False),
                        y=dict(show=False),
                        z=dict(show=False)
                    )
                )
            )

    def _create_sensors_arrow(self):
        """
        Add directional arrows representing sensor vectors to the 3D figure.

        This method iterates over the configured sensor vectors, determines
        their orientation, and adds corresponding arrow traces to the figure.
        Each arrow originates from the origin and points in the direction
        specified by the sensor vector, scaled appropriately.

        The arrows are styled based on configuration parameters such as
        arrow length ratio, line width, color, and line style.
        """
        for sensor in self.sensors:
            vector = sensor["vector"]
            arrow_vector = [0, 0, 0]
            try:
                position_idx = vector.index(next(filter(lambda x: x != 0, vector)))
            except StopIteration:
                continue  # Skip if the vector is [0, 0, 0]
            arrow_direction = 1 if vector[position_idx] > 0 else -1
            arrow_vector[position_idx] = arrow_direction * self._config.BOX_SIZE

            arrow_trace = go.Scatter3d(
                x=[0, self._config.SENSOR_ARROW_LENGTH_RATIO * arrow_vector[0]],
                y=[0, self._config.SENSOR_ARROW_LENGTH_RATIO * arrow_vector[1]],
                z=[0, self._config.SENSOR_ARROW_LENGTH_RATIO * arrow_vector[2]],
                mode='lines',
                line=dict(
                    width=self._config.SENSOR_ARROW_LINEWIDTH,
                    color=self._config.SENSOR_ARROW_COLOR,
                    dash=self._config.SENSOR_ARROW_LINESTYLE
                ),
                showlegend=False,
                hoverinfo='none'
            )
            self._fig.add_trace(arrow_trace)

    def _create_sensors_ellipse(self):
        """
        Draws 2D ellipses on the surfaces of the box, centered at the positions
        where the SENSOR_VECTORS intersect the box walls.

        Each ellipse is oriented perpendicular to the direction of the vector.
        """

        def _draw_sensor_ellipse(center, axis='x', color='white', radius_major=0.2, radius_minor=0.1, resolution=30):
            """
            Draws a filled ellipse using Mesh3d, oriented along given axis (x, y, or z),
            and centered at given position.
            """
            theta = np.linspace(0, 2 * np.pi, resolution)
            ellipse = np.array([
                [radius_major * np.cos(t), radius_minor * np.sin(t), 0] for t in theta
            ])

            if axis == 'x':
                ellipse = np.array([[0, x, y] for x, y, z in ellipse])
            elif axis == 'y':
                ellipse = np.array([[x, 0, y] for x, y, z in ellipse])
            elif axis == 'z':
                ellipse = np.array([[x, y, 0] for x, y, z in ellipse])

            ellipse += np.array(center)

            x, y, z = ellipse[:, 0], ellipse[:, 1], ellipse[:, 2]
            i = list(range(len(x)))
            j = [(k + 1) % len(x) for k in i]
            k = [len(x)] * len(x)

            x = np.append(x, center[0])
            y = np.append(y, center[1])
            z = np.append(z, center[2])

            if color:
                self._fig.add_trace(go.Mesh3d(
                    x=x, y=y, z=z,
                    i=i, j=j, k=k,
                    color=self._config.LEGEND_COLORS[color],
                    opacity=1,
                    flatshading=True,
                    showscale=False
                ))

            if color:
                self._fig.add_trace(go.Scatter3d(
                    x=np.append(x[:-1], x[0]),
                    y=np.append(y[:-1], y[0]),
                    z=np.append(z[:-1], z[0]),
                    mode='lines',
                    line=dict(color=self._config.SENSOR_COLOR_BORDER, width=self._config.SENSOR_LINE_WIDTH),
                    hoverinfo='none',
                    showlegend=False
                ))

        for it, sensor in enumerate(self.sensors):
            vector = sensor["vector"]
            vec = np.array(vector)
            center = vec * self._config.BOX_SIZE
            axis = ['x', 'y', 'z'][np.argmax(np.abs(vec))]

            color = sensor["color"]
            _draw_sensor_ellipse(
                center=center,
                axis=axis,
                color=color,
                radius_major=self._config.SENSOR_RADIUS_MAJOR,
                radius_minor=self._config.SENSOR_RADIUS_MINOR,
            )

    def _create_legend(self):
        """
        Add invisible 3D scatter traces to the figure to serve as legend entries
        for each sensor.

        Each trace is styled with the corresponding sensor's color and includes
        the sensor's value in its name. These traces are not plotted in the 3D
        space but appear in the legend to provide context for the sensor data.
        """
        for index, sensor in enumerate(self.sensors):
            color = sensor["color"]
            if color:
                legend_trace = go.Scatter3d(
                    x=[None], y=[None], z=[None],
                    mode='markers',
                    marker=dict(
                        color=self._config.LEGEND_COLORS[color],
                        size=10,
                        line=dict(
                            color='black',
                            width=1
                        )
                    ),
                    showlegend=True,
                    name=f'Sensor {index + 1}: {str(sensor['value'])}'
                )
                self._fig.add_trace(legend_trace)

    def on_update(self, light_vector, sensors_received):
        """
        Updates the sensor data and light vector based on received input,
        validates the data, and updates the corresponding elements in the plot.

        Parameters:
            light_vector (list or tuple): The new light direction vector.
            sensors_received (list): A list of sensor data dictionaries,
                each containing 'color', 'value' and 'vector'.

        If a sensor from the incoming data doesn't match an existing one,
        a warning is printed. After updating the values, the light vector
        and legend in the plot are refreshed.
        """
        for received in sensors_received:
            sensor = self._validate_sensor(received)
            if sensor:
                sensor["normalized_value"] = received["normalized_value"]
            else:
                print(f"[Warning] Sensor not matched: {received}")

        self._validate_light_vector(light_vector)
        self.light_vector = light_vector

        self._graph_update_light_vec()
        self._graph_update_legend()

    def _graph_update_light_vec(self):
        """
        Update or create the light vector arrow in the 3D figure.

        This method checks if a trace named 'light_vector' already exists in the
        figure. If it does, it updates the arrow coordinates to reflect the current
        light vector. Otherwise, it creates a new arrow trace to visualize the light
        vector direction.

        The arrow originates from the origin and points toward the direction of
        `self.light_vector`, using styling properties defined in the config.py.
        """
        vector_traces = [
            trace for trace in self._fig.data if trace.name == 'light_vector'
        ]

        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, self.light_vector[0]]
                arrow_trace.y = [0, self.light_vector[1]]
                arrow_trace.z = [0, self.light_vector[2]]
        else:
            arrow_properties = dict(
                line=dict(
                    color=self._config.LIGHT_VECTOR_COLOR,
                    width=self._config.LIGHT_VECTOR_WIDTH
                )
            )
            vec_trace = go.Scatter3d(
                x=[0, self.light_vector[0]],
                y=[0, self.light_vector[1]],
                z=[0, self.light_vector[2]],
                mode='lines',
                name='light_vector',
                showlegend=False,
                **arrow_properties
            )
            self._fig.add_trace(vec_trace)

    def _graph_update_legend(self):
        """
        Update the legend entries in the 3D figure to reflect current sensor values.
        """
        legends = [trace for trace in self._fig.data if trace.name is not None and 'Sensor' in trace.name]
        for it, legend in enumerate(legends):
            legend.name = f'Sensor {str(it + 1)}: {str(self.sensors[it]["value"])} V'

    def on_remove(self):
        """
        Removes the light vector and legend entries from the plot.

        This method is typically called when the visual representation of the
        current sensor data is no longer needed, effectively clearing it
        from the 3D graph.
        """
        self._graph_remove_light_vec()
        self._graph_remove_legend()

    def _graph_remove_light_vec(self):
        """
        Removes the light vector trace from the graph by resetting it to zero length.
        Additionally updates internal state by resetting the light vector to [0, 0, 0]
        and setting all sensor values to 0.
        """
        self.light_vector = [0, 0, 0]
        self.sensor_values = [0] * len(self.sensors)
        vector_traces = [trace for trace in self._fig.data if trace.name == 'light_vector']
        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, 0]
                arrow_trace.y = [0, 0]
                arrow_trace.z = [0, 0]

    def _graph_remove_legend(self):
        """
        Resets the labels of all sensor legends to the default value '0 V'.
        This can be used when removing the light vector or resetting the graph.
        """
        legends = [trace for trace in self._fig.data if trace.name is not None and 'Sensor' in trace.name]
        for it, legend in enumerate(legends):
            legend.name = f'Sensor {str(it + 1)}: {str(0)} V'

    @property
    def figure(self):
        """Retrieve the current Plotly Figure object.

        This property returns the figure associated with the Graph instance,
        allowing for further customization or rendering.
        """
        return self._fig

    def _validate_light_vector(self, vector):
        """
        Validates that the input is a 3D vector consisting of numeric values (int or float).

        Args:
            vector (list or tuple): A sequence of exactly three numeric values.

        Raises:
            TypeError: If the input is not a list or tuple, or contains non-numeric values.
            ValueError: If the input does not contain exactly three elements.
        """
        if not isinstance(vector, (list, tuple)):
            raise TypeError("light_vector must be a list or tuple.")
        if len(vector) != 3:
            raise ValueError("light_vector must contain exactly 3 elements.")
        if not all(isinstance(x, (float, int)) for x in vector):
            raise TypeError("All elements in light_vector must be numeric (int or float).")

    def _validate_sensor(self, received):
        """
        Finds and returns the matching sensor from the stored sensors list.

        The matching is based on both the color and vector attributes.
        If no matching sensor is found, returns None.

        Args:
            received (dict): A dictionary containing 'color' and 'vector' keys
                             representing the received sensor data.
git remote -v  
        Returns:
            dict or None: The matched sensor dictionary if found, otherwise None.
        """

        return next(
            (
                sensor for sensor in self.sensors
                if sensor["color"] == received["color"] and sensor["vector"] == received["vector"]
            ),
            None
        )