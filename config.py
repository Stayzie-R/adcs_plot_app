

DEBUG = True
RELOAD_INTERVAL = 500

BOX_SIZE = 1
BOX_COLOR = 'black'
BOX_LINEWIDTH = .7
BOX_LINESTYLE = 'solid'

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
SENSOR_RADIUS_MINOR = .65
SENSOR_RADIUS_MAJOR = .95

SENSOR_ARROW_LINEWIDTH = 3.0
SENSOR_ARROW_LINESTYLE = "dash"
SENSOR_ARROW_COLOR = "gray"
SENSOR_ARROW_LENGTH_RATIO = 1.5

LIGHT_VECTOR_COLOR = "red"
LIGHT_VECTOR_WIDTH = 4
LIGHT_VECTOR_TARGET_LENGTH = 10 * BOX_SIZE
