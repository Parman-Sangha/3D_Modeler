"""
JSON Schema definitions for 3D Modeler Pro output structure.
Ensures all generated JSON follows the required format.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class RoomType(Enum):
    KITCHEN = "kitchen"
    BEDROOM = "bedroom"
    BATHROOM = "bathroom"
    LIVING = "living"
    HALLWAY = "hallway"
    STORAGE = "storage"


class PrivacyLevel(Enum):
    PUBLIC = "public"
    SEMI_PRIVATE = "semi-private"
    PRIVATE = "private"


class OpeningType(Enum):
    DOOR = "door"
    WINDOW = "window"


class Theme(Enum):
    SCANDINAVIAN = "scandinavian"
    INDUSTRIAL = "industrial"
    MINIMALIST = "minimalist"
    MODERN = "modern"
    RUSTIC = "rustic"


@dataclass
class Meta:
    version: str = "1.0"
    unit_system: str = "metric"
    scale: float = 1.0
    generated_by: str = "3D Modeler Pro"
    confidence: float = 0.0


@dataclass
class House:
    type: str = "residential"
    footprint_shape: str = "rectangle"
    total_area_m2: float = 0.0
    width_m: float = 0.0
    depth_m: float = 0.0
    ceiling_height_m: float = 2.7
    floors: int = 1


@dataclass
class Level:
    level_id: str = "ground_floor"
    elevation_m: float = 0.0
    height_m: float = 2.7


@dataclass
class RoomBounds:
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    depth: float = 0.0


@dataclass
class Room:
    room_id: str = ""
    name: str = ""
    level_id: str = "ground_floor"
    area_m2: float = 0.0
    shape: str = "rectangle"
    bounds: RoomBounds = None
    adjacent_rooms: List[str] = None
    room_type: str = ""
    privacy_level: str = "public"
    
    def __post_init__(self):
        if self.bounds is None:
            self.bounds = RoomBounds()
        if self.adjacent_rooms is None:
            self.adjacent_rooms = []


@dataclass
class Wall:
    wall_id: str = ""
    start: List[float] = None
    end: List[float] = None
    height_m: float = 2.7
    thickness_m: float = 0.2
    level_id: str = "ground_floor"
    load_bearing: bool = True
    
    def __post_init__(self):
        if self.start is None:
            self.start = [0.0, 0.0]
        if self.end is None:
            self.end = [0.0, 0.0]


@dataclass
class Opening:
    opening_id: str = ""
    type: str = "door"
    wall_id: str = ""
    position_ratio: float = 0.5
    width_m: float = 0.9
    height_m: float = 2.1
    swing: str = "none"
    transparent: bool = False


@dataclass
class Furniture:
    furniture_id: str = ""
    type: str = ""
    room_id: str = ""
    position: List[float] = None
    rotation_deg: float = 0.0
    scale: float = 1.0
    preset: str = ""
    
    def __post_init__(self):
        if self.position is None:
            self.position = [0.0, 0.0]


@dataclass
class Accessibility:
    wheelchair: bool = False
    door_min_width_m: float = 0.9


@dataclass
class Constraints:
    budget_level: str = "medium"
    accessibility: Accessibility = None
    region_code: str = "NA"
    
    def __post_init__(self):
        if self.accessibility is None:
            self.accessibility = Accessibility()


@dataclass
class Styles:
    theme: str = "modern"
    color_palette: List[str] = None
    material_bias: Dict[str, float] = None
    
    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = ["#ffffff", "#cfcfcf", "#8a8a8a"]
        if self.material_bias is None:
            self.material_bias = {"wood": 0.5, "metal": 0.3, "concrete": 0.2}


@dataclass
class Exports:
    formats: List[str] = None
    include_textures: bool = True
    include_furniture: bool = True
    optimize_mesh: bool = True
    
    def __post_init__(self):
        if self.formats is None:
            self.formats = ["glb", "fbx", "obj", "usd", "blend"]


class SceneSchema:
    """Main scene structure following the required JSON format."""
    
    def __init__(self):
        self.meta = Meta()
        self.house = House()
        self.levels: List[Level] = []
        self.rooms: List[Room] = []
        self.walls: List[Wall] = []
        self.openings: List[Opening] = []
        self.furniture: List[Furniture] = []
        self.materials: Dict[str, str] = {}
        self.styles = Styles()
        self.constraints = Constraints()
        self.exports = Exports()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "meta": asdict(self.meta),
            "house": asdict(self.house),
            "levels": [asdict(level) for level in self.levels],
            "rooms": [self._room_to_dict(room) for room in self.rooms],
            "walls": [asdict(wall) for wall in self.walls],
            "openings": [asdict(opening) for opening in self.openings],
            "furniture": [asdict(furn) for furn in self.furniture],
            "materials": self.materials,
            "styles": asdict(self.styles),
            "constraints": self._constraints_to_dict(),
            "exports": asdict(self.exports)
        }
    
    def _room_to_dict(self, room: Room) -> Dict[str, Any]:
        """Convert room with nested bounds to dict."""
        return {
            "room_id": room.room_id,
            "name": room.name,
            "level_id": room.level_id,
            "area_m2": room.area_m2,
            "shape": room.shape,
            "bounds": asdict(room.bounds),
            "adjacent_rooms": room.adjacent_rooms,
            "room_type": room.room_type,
            "privacy_level": room.privacy_level
        }
    
    def _constraints_to_dict(self) -> Dict[str, Any]:
        """Convert constraints with nested accessibility to dict."""
        return {
            "budget_level": self.constraints.budget_level,
            "accessibility": asdict(self.constraints.accessibility),
            "region_code": self.constraints.region_code
        }
