

DEBUG = False
RELOAD_INTERVAL = 500


GRAPH_3D_TITLE = "ADCS 3D Visualization"
GRAPH_2D_TITLE = "Top View Projection"

LEGEND_TITLE = "Light Sensor Readings"
LIGHT_VEC_ANNOT = "Light Vector"

BOX_SIZE = 1
BOX_COLOR = 'black'
BOX_LINEWIDTH = 1
BOX_LINESTYLE = 'solid'

CUBE_LINEWIDTH = 0.8
CUBE_COLOR = 'black'

ALLOW_PLANE = True
PLANE_SCALE_FACTOR = 2
PLANE_COLOR = 'gray'

SENSORS = {
    "white":(1, 0, 0),
    "yellow":(0, 1, 0),
    "brown":(-1, 0, 0),
    "green":(0, -1, 0),
    "orange":(0, 0, 1),
    "":(0, 0, -1)
}

LEGEND_COLORS = {
    "white": "#FFFFFF",
    "yellow": "#FFFF00",
    "brown": "#8B4513",
    "green": "#228B22",
    "orange": "#FF8C00",
    "": ""
}

SENSOR_COLOR_DEFAULT = "white"
SENSOR_COLOR_BORDER = 'black'
SENSOR_LINE_WIDTH = .5
SENSOR_RADIUS_MINOR = .1
SENSOR_RADIUS_MAJOR = .15

SENSOR_ARROW_LINEWIDTH = 5.0
SENSOR_ARROW_LINESTYLE = "dash"
SENSOR_ARROW_COLOR = "gray"
SENSOR_ARROW_LENGTH_RATIO = 1.5

LIGHT_VECTOR_COLOR = "red"
LIGHT_VECTOR_WIDTH = 4
LIGHT_VECTOR_TARGET_LENGTH = 1.5 * BOX_SIZE

LIGHT_VECTOR_COLOR_2D = "red"
LIGHT_VECTOR_WIDTH_2D = 2
LIGHT_VECTOR_TARGET_LENGTH_2D = .8 * BOX_SIZE