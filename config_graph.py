from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass
class TitleConfig:
    TITLE_3D: str = "ADCS 3D Visualization"
    TITLE_2D: str = "Top View Projection"
    TEXT_SIZE: int = 18


@dataclass
class LegendConfig:
    TITLE: str = "Sensor Readings"
    TITLE_SIZE: int = 14
    TITLE_COLOR: str = "black"
    ITEM_SIZE: int = 12
    ITEM_COLOR: str = "black"


@dataclass
class LegendLightVectorConfig:
    TITLE: str = "Light Vector"
    TITLE_SIZE: int = 14
    TITLE_COLOR: str = "black"
    ITEM_SIZE: int = 12
    ITEM_COLOR: str = "black"


@dataclass
class BoxConfig:
    SIZE: float = 1
    COLOR: str = "black"
    LINEWIDTH_3D: float = 1.5
    LINESTYLE: str = "solid"
    LINEWIDTH_2D: float = 0.8


@dataclass
class PlaneConfig:
    ALLOW: bool = True
    SCALE_FACTOR: float = 2
    COLOR: str = "gray"


@dataclass
class SensorsConfig:
    COLOR_DEFAULT: str = "white"
    COLOR_BORDER: str = "black"
    LINE_WIDTH: float = 0.5
    RADIUS_MINOR: float = 0.1
    RADIUS_MAJOR: float = 0.15


@dataclass
class ArrowConfig:
    LINEWIDTH: float = 5.0
    LINESTYLE: str = "dash"
    COLOR: str = "gray"
    LENGTH_RATIO: float = 1.5


@dataclass
class LightVectorConfig:
    COLOR: str = "red"
    WIDTH_3D: float = 4
    TARGET_LENGTH_3D: float = 1.5  # this will be updated dynamically from box.SIZE
    WIDTH_2D: float = 2
    TARGET_LENGTH_2D: float = 0.8  # this will be updated dynamically from box.SIZE


class Config_Graph:
    def __init__(self):
        self.title = TitleConfig()
        self.legend = LegendConfig()
        self.legend_light_vector = LegendLightVectorConfig()
        self.box = BoxConfig()
        self.plane = PlaneConfig()
        self.sensor = SensorsConfig()
        self.arrow = ArrowConfig()

        self.light_vector = LightVectorConfig(
            TARGET_LENGTH_3D=1.5 * self.box.SIZE,
            TARGET_LENGTH_2D=0.8 * self.box.SIZE
        )

        self.legend_colors: Dict[str, str] = {
            "white": "#FFFFFF",
            "yellow": "#FFFF00",
            "brown": "#8B4513",
            "green": "#228B22",
            "orange": "#FF8C00",
            "": ""
        }

        self.SENSORS: Dict[str, Tuple[int, int, int]] = {
            "white": (1, 0, 0),
            "yellow": (0, 1, 0),
            "brown": (-1, 0, 0),
            "green": (0, -1, 0),
            "orange": (0, 0, 1),
            "": (0, 0, -1)
        }
