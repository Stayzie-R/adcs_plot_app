from itertools import combinations, product
from webbrowser import open_new_tab

import plotly.graph_objs as go
import numpy as np

from config_graph import Config


class Graph:
    """
    Class to create and manage a 3D scatter plot figure.
    """
    def __init__(self):
        """
        Initializes the Graph object:
        - Loads configuration from config_graph.
        - Initializes the light vector and sensor metadata.
        - Prepares and configures empty 3D and 2D Plotly figures.
        """
        self._config = Config()

        self.light_vector = [0.0, 0.0, 0.0]

        self.sensors = [
            {
                "color": color,
                "vector": vector,
                "value": 0.0
            }
            for color, vector in self._config.SENSORS.items()
        ]

        self._fig_3d = go.Figure()
        self._configure_graph_3d()
        self._init_3d()

        self._fig_2d = go.Figure()
        self._configure_graph_2d()
        self._init_2d()

    def _configure_graph_3d(self):
        """
        Configure the layout and interaction behavior of the 3D Plotly graph.
        """
        self._fig_3d.update_layout(
            title=dict(
                text=self._config.title.TITLE_3D,
                font=dict(size=18),
                x=0.5,
                y=0.8,  # Adjust the title's vertical position (0 is bottom, 1 is top)
                xanchor='right',
                yanchor='top'
            ),
            uirevision='constant',  # Keeps the layout intact when the data is updated
            dragmode='turntable',
            showlegend=False,
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
                    eye=dict(x=1.03, y=-1.54, z=0.45)
                )
            ),
            width=500,                           # Width of the graph in pixels
            height=500,                          # Height of the graph in pixels
            margin=dict(l=0, r=0, t=50, b=0),    # Margins around the graph
            hovermode=False,                     # Hover efekt
        )
        
    def _configure_graph_2d(self):
        """
        Configure the layout and styling of the 2D Plotly graph.
        """
        zoom_factor = 1
        limit = self._config.box.SIZE / zoom_factor
        self._fig_2d.update_layout(
            title=dict(
                text=self._config.title.TITLE_3D,
                font=dict(size=self._config.title.TEXT_SIZE),
                x=0.35,
                y=0.8,
                xanchor='right',
                yanchor='top'
            ),
            showlegend=True,
            dragmode=False,
            xaxis=dict(
                range=[-limit, limit],
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                visible=False,
                fixedrange=True,
                scaleanchor="y",
                scaleratio=1,
            ),
            yaxis=dict(
                range=[-limit, limit],
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                visible=False,
                fixedrange=True
            ),
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            ),
            width=600,
            height=500,
            margin=dict(l=0, r=300, t=50, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                x=1.05,
                y=0,
                traceorder='normal',
                font=dict(color=self._config.legend.ITEM_COLOR, size=self._config.legend.ITEM_SIZE),
                title=dict(
                    text=self._config.legend.TITLE,
                    font=dict(size=self._config.legend.TITLE_SIZE, color=self._config.legend.TITLE_COLOR),
                    side="top"
                ),
                itemclick=False,
                itemdoubleclick=False,
            ),
        )

    def _init_3d(self):
        """
        Plots all static elements of the scene of 3D graph , including the box, base plane,
        sensor direction arrows, sensor points.

        This method is called once during initialization to draw static components
        that do not change dynamically during updates.
        """
        self._create_box_3d()
        self._create_plane_3d()
        self._create_sensors_arrow_3d()
        self._create_sensors_ellipse_3d()

    def _init_2d(self):
        """
        Plots all static elements of the scene of 2D , including the box, base plane,
        sensor direction arrows, sensor points, legend and light_vector tracer.

        This method is called once during initialization to draw static components
        that do not change dynamically during updates.
        """
        self._create_plane_2d()
        self._create_cube_2d()
        self._create_sensor_arrow_2d()
        self._create_sensors_ellipse_2d()

        self._create_legend()
        self._crete_light_vec_annotation()

    def _create_box_3d(self):
        """
        Adds a static 3D box outline to the figure.

        This method computes and plots the edges of a cube defined by the
        radius values in all three dimensions. It is intended for internal
        use to visualize static reference geometry within the 3D scene.
        The box's appearance is controlled by configuration parameters in
        config_graph.py.
        """
        radius = [-self._config.box.SIZE, self._config.box.SIZE]
        for s, e in combinations(np.array(list(product(radius, radius, radius))), 2):
            if np.sum(np.abs(s - e)) == radius[1] - radius[0]:
                pos = [list(pair) for pair in zip(s, e)]
                self._fig_3d.add_trace(
                    go.Scatter3d(
                        x=pos[0], y=pos[1], z=pos[2],
                        mode='lines',
                        line=dict(color=self._config.box.COLOR,
                                  width=self._config.box.LINEWIDTH_3D,
                                  dash=self._config.box.LINESTYLE),
                        showlegend=False,
                        hoverinfo='none'
                    )
                ),

    def _create_cube_2d(self):
        """
        Adds a static 2D square (representing the top view of a cube) to the 2D figure.

        The method calculates corner coordinates based on half the box size
        and draws the square using a line trace. Visual appearance is controlled
        by parameters in config_graph.py.
        """
        radius = [-self._config.box.SIZE/2, self._config.box.SIZE/2]
        x_values = np.array([radius[0], radius[1], radius[1], radius[0], radius[0]])
        y_values = np.array([radius[0], radius[0], radius[1], radius[1], radius[0]])

        self._fig_2d.add_trace(go.Scatter(
            x=x_values, y=y_values, mode='lines',
            line=dict(color=self._config.box.COLOR, width=self._config.box.LINEWIDTH_2D),
            showlegend=False
        ))
        
    def _create_plane_3d(self):
        """
        Adds a semi-transparent horizontal plane to the 3D figure.

        This method generates a flat surface positioned at a fixed Z-level,
        used to represent a reference plane within the 3D scene.
        The plane's visibility and appearance are controlled by configuration
        parameters in config.py.
        """
        if self._config.plane.ALLOW:
            radius = [-self._config.box.SIZE, self._config.box.SIZE]
            x_values = self._config.plane.SCALE_FACTOR * np.linspace(radius, radius, 1)
            y_values = self._config.plane.SCALE_FACTOR * np.linspace(radius, radius, 1)
            x_mesh, y_mesh = np.meshgrid(x_values, y_values)
            z_mesh = np.ones_like(x_mesh) * -self._config.box.SIZE
            self._fig_3d.add_trace(
                go.Surface(
                    x=x_mesh, y=y_mesh, z=z_mesh,
                    colorscale=[self._config.plane.COLOR] * len(x_mesh.flatten()),
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

    def _create_plane_2d(self):
        """
        Adds a semi-transparent square plane to the 2D scene.

        This plane serves as a visual reference, centered at the origin,
        and its visibility and size are controlled by configuration settings.
        """
        if self._config.plane.ALLOW:
            radius = self._config.box.SIZE/3 * self._config.plane.SCALE_FACTOR
            x_values = [-radius, radius, radius, -radius, -radius]
            y_values = [-radius, -radius, radius, radius, -radius]

            self._fig_2d.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                fill='toself',
                fillcolor="#F5F5F5",
                line=dict(color='rgba(0,0,0,0)'),
                hoverinfo='none',
                showlegend=False
            ))

    def _create_sensors_arrow_3d(self):
        """
        Adds directional arrows to the 3D figure representing sensor vectors.

        Each arrow starts at the origin and points in the configured sensor direction,
        scaled relative to the box size. Styling is defined in the configuration.
        """
        for sensor in self.sensors:
            vector = sensor["vector"]
            arrow_vector = [0, 0, 0]
            try:
                position_idx = vector.index(next(filter(lambda x: x != 0, vector)))
            except StopIteration:
                continue  # Skip if the vector is [0, 0, 0]
            arrow_direction = 1 if vector[position_idx] > 0 else -1
            arrow_vector[position_idx] = arrow_direction * self._config.box.SIZE

            arrow_trace = go.Scatter3d(
                x=[0, self._config.arrow.LENGTH_RATIO * arrow_vector[0]],
                y=[0, self._config.arrow.LENGTH_RATIO * arrow_vector[1]],
                z=[0, self._config.arrow.LENGTH_RATIO * arrow_vector[2]],
                mode='lines',
                line=dict(
                    width=self._config.arrow.LINEWIDTH,
                    color=self._config.arrow.COLOR,
                    dash=self._config.arrow.LINESTYLE
                ),
                showlegend=False,
                hoverinfo='none'
            )
            self._fig_3d.add_trace(arrow_trace)

    def _create_sensor_arrow_2d(self):
        """
        Adds dashed arrows from the center of the cube outward to visualize sensor directions.
        Each arrow extends 1.5 times the box size beyond the edge.
        """
        length = self._config.box.SIZE * 1.5

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]

        for nx, ny in directions:
            ex, ey = nx * length / 2, ny * length / 2
            self._fig_2d.add_trace(go.Scatter(
                x=[0, ex], y=[0, ey],
                mode='lines',
                line=dict(
                    color='black',
                    width=0.5,
                    dash="dot"
                ),
                showlegend=False,
                hoverinfo='none'
            ))

    def _create_sensors_ellipse_3d(self):
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
                self._fig_3d.add_trace(go.Mesh3d(
                    x=x, y=y, z=z,
                    i=i, j=j, k=k,
                    color=self._config.legend_colors[color],
                    opacity=1,
                    flatshading=True,
                    showscale=False
                ))

            if color:
                self._fig_3d.add_trace(go.Scatter3d(
                    x=np.append(x[:-1], x[0]),
                    y=np.append(y[:-1], y[0]),
                    z=np.append(z[:-1], z[0]),
                    mode='lines',
                    line=dict(color=self._config.sensor.COLOR_BORDER, width=self._config.sensor.LINE_WIDTH),
                    hoverinfo='none',
                    showlegend=False
                ))

        for it, sensor in enumerate(self.sensors):
            vector = sensor["vector"]
            vector = self.convert_real_to_dash_coordinates(vector)
            vec = np.array(vector)
            center = vec * self._config.box.SIZE
            axis = ['x', 'y', 'z'][np.argmax(np.abs(vec))]

            color = sensor["color"]
            _draw_sensor_ellipse(
                center=center,
                axis=axis,
                color=color,
                radius_major=self._config.sensor.RADIUS_MAJOR,
                radius_minor=self._config.sensor.RADIUS_MINOR,
            )

    def _create_sensors_ellipse_2d(self):
        """
       Draws 2D ellipses (representing sensors) at the centers of each wall where sensors are located.

       The center of each ellipse is calculated based on the sensor's direction vector, and the final plot includes
       these ellipses in the 2D visualization with the appropriate color and borders.
       """
        def create_ellipse(center_x, center_y, radius_x, radius_y, resolution=100):
            theta = np.linspace(0, 2 * np.pi, resolution)
            x = center_x + radius_x * np.cos(theta)
            y = center_y + radius_y * np.sin(theta)
            return x, y


        for color, vector in self._config.SENSORS.items():
            if not color:
                continue
            x_dir, y_dir, z_dir = self.convert_real_to_dash_coordinates(vector)
            center_x = x_dir * self._config.box.SIZE/2
            center_y = y_dir * self._config.box.SIZE/2

            if center_x == 0:
                radius_major = self._config.box.SIZE * .06
                radius_minor = self._config.box.SIZE * .04
            else:
                radius_major = self._config.box.SIZE * .04
                radius_minor = self._config.box.SIZE * .06

            x, y = create_ellipse(center_x, center_y, radius_major, radius_minor)

            self._fig_2d.add_trace(go.Scatter(
                x=x, y=y,
                mode='lines',
                fill='toself',
                fillcolor=self._config.legend_colors.get(color, 'white'),
                line=dict(color='black', width=1),
                name=color,
                showlegend=False,
            ))

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
                        color=self._config.legend_colors[color],
                        size=10,
                        line=dict(
                            color='black',
                            width=1
                        )
                    ),
                    showlegend=True,
                    name = 'Sensor ' + str(index + 1) + ': ' + str(sensor['value'])
                )
                self._fig_2d.add_trace(legend_trace)

    def _crete_light_vec_annotation(self):
        """
        Manually adds a custom annotation for the light vector value in the 2D figure.

        Since a second legend is not supported in 2D figures, this method creates a
        custom annotation to display the light vector’s value. The annotation consists of:
        - The light vector value.
        - A line (styled like a marker) used to associate the light vector value
          with the red-colored vector in the figure.

        The position of this annotation is chosen manually and placed directly above the existing legend.
        """
        legend_position = self._fig_2d.layout.legend
        base_x = legend_position.x
        base_y = legend_position.y + .45

        annotations = [
            dict(
                text=self._config.legend_light_vector.TITLE,
                xref="paper", yref="paper",
                x=base_x, y=base_y,
                showarrow=False,
                xanchor='left',
                yanchor='top',
                font=dict(size=self._config.legend_light_vector.TITLE_SIZE, color=self._config.legend_light_vector.TITLE_COLOR),
            ),
            dict(
                text= str([round(num, 2) for num in self.light_vector]),
                xref="paper", yref="paper",
                x=base_x+0.13, y=base_y - 0.065,
                showarrow=False,
                bgcolor="rgba(0,0,0,0)",
                xanchor='left',
                font=dict(size=self._config.legend_light_vector.ITEM_SIZE, color=self._config.legend_light_vector.ITEM_COLOR),
            ),
        ]
        for annot in annotations:
            self._fig_2d.add_annotation(**annot)


        position_x_end =  0.055
        self._fig_2d.add_shape(
            type="line",
            x0=base_x + 0.04, y0=base_y - 0.07,
            x1=base_x + 0.04 + position_x_end, y1=base_y - 0.07,
            xref="paper", yref="paper",
            line=dict(
                color=self._config.light_vector.COLOR,
                width=3.5,
            ),
            layer="above"
        )

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
                sensor["value"] = received["value"]
            else:
                print(f"[Warning] Sensor not matched: {received}")

        self._validate_light_vector(light_vector)
        self.light_vector = light_vector

        self._update_light_vec_3d()
        self._update_light_vec_2d()

        self._update_legend()
        self._update_light_vec_annotation()

    def _update_light_vec_3d(self):
        """
        Updates or creates the light vector arrow in the 3D figure.

        If the 'light_vector_3d' trace exists, it updates its coordinates to reflect
        the current light vector. If it doesn't exist, it creates a new arrow from
        the origin pointing in the direction of `self.light_vector`.

        The arrow's length is scaled according to the config, and it uses defined styles
        in config_graph.py.
        """
        target_length = self._config.light_vector.TARGET_LENGTH_3D
        vec = self.convert_real_to_dash_coordinates(self.light_vector)
        vec = np.array(vec)
        vec_len = np.linalg.norm(vec)

        if vec_len != 0:
            scaled_vec = vec / vec_len * target_length
        else:
            scaled_vec = vec

        vector_traces = [
            trace for trace in self._fig_3d.data if trace.name == 'light_vector_3d'
        ]


        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, scaled_vec[0]]
                arrow_trace.y = [0, scaled_vec[1]]
                arrow_trace.z = [0, scaled_vec[2]]
        else:
            arrow_properties = dict(
                line=dict(
                    color=self._config.light_vector.COLOR,
                    width=self._config.light_vector.WIDTH
                )
            )
            vec_trace = go.Scatter3d(
                x=[0, scaled_vec[0]],
                y=[0, scaled_vec[1]],
                z=[0, scaled_vec[2]],
                mode='lines',
                name='light_vector_3d',
                showlegend=False,
                **arrow_properties
            )
            self._fig_3d.add_trace(vec_trace)

    def _update_light_vec_2d(self):
        """
        Update or create the light vector arrow in the 2D figure.

        This method checks if a trace named 'light_vector_2d' already exists in the
        figure. If it does, it updates the arrow coordinates to reflect the current
        light vector. Otherwise, it creates a new arrow trace to visualize the light
        vector direction in 2D.

        The arrow originates from the origin and points toward the direction of
        `self.light_vector`, using styling properties defined in the config.py.
        """
        target_length = self._config.light_vector.TARGET_LENGTH_2D
        vec = self.convert_real_to_dash_coordinates(self.light_vector)
        vec = np.array(vec)
        vec_len = np.linalg.norm(vec[:2])

        if vec_len != 0:
            scaled_vec = vec[:2] / vec_len * target_length
        else:
            scaled_vec = vec[:2]

        vector_traces = [
            trace for trace in self._fig_2d.data if trace.name == 'light_vector_2d'
        ]

        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, scaled_vec[0]]
                arrow_trace.y = [0, scaled_vec[1]]
        else:
            arrow_properties = dict(
                line=dict(
                    color=self._config.light_vector.COLOR,
                    width=self._config.light_vector.WIDTH
                )
            )
            vec_trace = go.Scatter(
                x=[0, scaled_vec[0]],
                y=[0, scaled_vec[1]],
                mode='lines',
                name='light_vector_2d',
                showlegend=False,
                **arrow_properties
            )
            self._fig_2d.add_trace(vec_trace)

    def _update_legend(self):
        """
        Update the legend entries in the 2D figure to reflect current sensor values.

        The legend entries are updated with the corresponding sensor values in volts.
        """
        legends = [trace for trace in self._fig_2d.data if trace.name is not None and 'Sensor' in trace.name]
        for it, legend in enumerate(legends):
            legend.name = 'Sensor ' + str(it + 1) + ': ' + str(self.sensors[it]["value"]) + ' V'

    def _update_light_vec_annotation(self):
        """
        Update the light vector annotation in the 2D figure.

        The light vector annotation is updated based on the current `self.light_vector` value.
        """
        for annotation in self._fig_2d.layout.annotations:
            if isinstance(annotation.text, str) and annotation.text.strip().startswith("[") and annotation.text.strip().endswith("]"):
                annotation.update(text=str(str([round(num, 2) for num in self.light_vector])))
                break

    def on_remove(self):
        """
        Removes the light vector and legend entries from the plot.

        The light vector is reset, and the sensors are updated with the current values.
        """
        light_vector = [0.0, 0.0, 0.0]
        sensors = [
            {
                "color": sensor["color"],
                "vector": sensor["vector"],
                "value": round(sensor["value"], 0)
            }
            for sensor in self.sensors
    
        ]
        self.on_update(light_vector, sensors)
        #self._remove_light_vec_3d()
        #self._remove_light_vec_2d()
        #self._remove_legend()

    def _remove_light_vec_3d(self):
        """
        Removes the light vector trace from the graph by resetting it to zero length.
        Additionally updates internal state by resetting the light vector to [0, 0, 0]
        and setting all sensor values to 0.
        """
        vector_traces = [trace for trace in self._fig_3d.data if trace.name == 'light_vector_3d']
        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, 0]
                arrow_trace.y = [0, 0]
                arrow_trace.z = [0, 0]

    def _remove_light_vec_2d(self):
        """
        Removes the light vector trace from the 2D plot by resetting its coordinates to zero.
        This method is called when the light vector needs to be removed from the 2D plot.
        """
        vector_traces = [trace for trace in self._fig_2d.data if trace.name == 'light_vector_2d']
        if vector_traces:
            for arrow_trace in vector_traces:
                arrow_trace.x = [0, 0]
                arrow_trace.y = [0, 0]

    def _remove_legend(self):
        """
        Resets the labels of all sensor legends to the default value '0 V'.
        This can be used when removing the light vector or resetting the graph.
        """
        legends = [trace for trace in self._fig_2d.data if trace.name is not None and 'Sensor' in trace.name]
        for it, legend in enumerate(legends):
            legend.name = 'Sensor ' + str(it + 1) + ': ' + str(0) + ' V'

    def _remove_light_vec_annotation(self):
        """
        Resets the light vector annotation in the 2D plot to its default value '[0.0, 0.0, 0.0]'.
        This can be used when the light vector is removed, ensuring the annotation shows the
        correct default state.
        """
        for i, annotation in enumerate(self._fig_2d.layout.annotations):
            if (
                    isinstance(annotation.text, str) and
                    annotation.text.strip().startswith("[") and
                    annotation.text.strip().endswith("]")
            ):
                new_annotation = annotation.to_plotly_json()
                new_annotation["text"] = str([0.0, 0.0, 0.0])
                annotations = list(self._fig_2d.layout.annotations)
                annotations[i] = new_annotation
                self._fig_2d.update_layout(annotations=annotations)
                break

    @property
    def figure_3d(self):
        """
        Get the current šD Plotly figure for rendering.

        Returns:
            plotly.graph_objs.Figure: The 3D Plotly figure object.
        """
        return self._fig_3d

    @property
    def figure_2d(self):
        """
        Get the current 2D Plotly figure for rendering.

        Returns:
            plotly.graph_objs.Figure: The 2D Plotly figure object.
        """
        return self._fig_2d

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

        Returns:
            dict or None: The matched sensor dictionary if found, otherwise None.
        """

        return next(
            (
                sensor for sensor in self.sensors
                if sensor["color"] == received["color"] and sensor["vector"] == tuple(received["vector"])

            ),
            None
        )

    def convert_real_to_dash_coordinates(self, real_vector):
        """
        Converts a real-world vector into Plotly Dash 3D coordinate system.

        Plotly Dash uses a different 3D coordinate system compared to typical
        real-world (physics-based) conventions:
          - In real-world systems:
              * X axis points right
              * Y points towards the observer (out of the screen)
              * Z axis points up
          - In Dash 3D plots:
              * X axis points right
              * Y axis points INTO the screen
              * Z axis points up
        Args:
            real_vector (tuple or list of float):
                The real-world vector (x, y, z) to be converted.

        Returns:
            tuple of float:
                Converted vector (dash_x, dash_y, dash_z) suitable for Dash plotting.
        """

        if len(real_vector) == 3:
            x_real, y_real, z_real = real_vector
            return (x_real, -y_real, z_real)
        else:
            x_real, y_real = real_vector
            return (x_real, -y_real)
