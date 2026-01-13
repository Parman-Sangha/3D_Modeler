"""
3D Modeler Pro - Core architectural reasoning and JSON generation engine.
Converts natural language descriptions into structured architectural scene JSON.
"""

import json
import re
from typing import Dict, List, Any, Optional
from schema import (
    SceneSchema, Meta, House, Level, Room, RoomBounds, Wall, Opening,
    Furniture, Styles, Constraints, Exports, RoomType, PrivacyLevel
)


class ModelerPro:
    """
    Main engine for generating architectural scene JSON from natural language.
    """
    
    def __init__(self):
        self.schema = SceneSchema()
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """Set up default scene structure."""
        self.schema.meta = Meta()
        self.schema.house = House()
        self.schema.levels = [Level()]
        self.schema.rooms = []
        self.schema.walls = []
        self.schema.openings = []
        self.schema.furniture = []
        self.schema.materials = {}
        self.schema.styles = Styles()
        self.schema.constraints = Constraints()
        self.schema.exports = Exports()
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate architectural scene JSON from natural language prompt.
        
        Args:
            prompt: Natural language description of the space
            **kwargs: Additional parameters (style, constraints, etc.)
        
        Returns:
            Valid JSON string (no markdown, no comments)
        """
        self._initialize_defaults()
        
        # Parse prompt for architectural requirements
        self._parse_prompt(prompt, **kwargs)
        
        # Generate structure
        self._generate_structure()
        
        # Add furniture based on room types
        self._add_furniture()
        
        # Apply materials
        self._apply_materials()
        
        # Validate and return JSON
        scene_dict = self.schema.to_dict()
        return json.dumps(scene_dict, indent=2, ensure_ascii=False)
    
    def _parse_prompt(self, prompt: str, **kwargs):
        """Extract architectural requirements from prompt."""
        prompt_lower = prompt.lower()
        
        # Detect room types
        rooms_to_create = []
        if "bedroom" in prompt_lower or "bed" in prompt_lower:
            count = self._extract_number(prompt_lower, ["bedroom", "bed"])
            for i in range(max(1, count)):
                rooms_to_create.append(("bedroom", f"bedroom_{i+1}"))
        
        if "bathroom" in prompt_lower or "bath" in prompt_lower:
            count = self._extract_number(prompt_lower, ["bathroom", "bath"])
            for i in range(max(1, count)):
                rooms_to_create.append(("bathroom", f"bathroom_{i+1}"))
        
        if "kitchen" in prompt_lower:
            rooms_to_create.append(("kitchen", "kitchen_1"))
        
        if "living" in prompt_lower or "lounge" in prompt_lower:
            rooms_to_create.append(("living", "living_room_1"))
        
        # Always add at least a living room if nothing specified
        if not rooms_to_create:
            rooms_to_create.append(("living", "living_room_1"))
        
        # Detect style
        if "scandinavian" in prompt_lower:
            self.schema.styles.theme = "scandinavian"
        elif "industrial" in prompt_lower:
            self.schema.styles.theme = "industrial"
        elif "minimalist" in prompt_lower:
            self.schema.styles.theme = "minimalist"
        elif "rustic" in prompt_lower:
            self.schema.styles.theme = "rustic"
        else:
            self.schema.styles.theme = "modern"
        
        # Store rooms to create
        self._rooms_to_create = rooms_to_create
        
        # Detect size constraints
        area_match = re.search(r'(\d+)\s*(?:sqm|m2|square\s*meters?)', prompt_lower)
        if area_match:
            self.schema.house.total_area_m2 = float(area_match.group(1))
    
    def _extract_number(self, text: str, keywords: List[str]) -> int:
        """Extract number associated with keywords."""
        # Word to number mapping
        word_numbers = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        
        for keyword in keywords:
            # Try numeric patterns: "2 bedroom", "2-bedroom", "2bedroom"
            pattern = rf'(\d+)[\s-]*{keyword}'
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
            
            # Try word numbers: "two bedroom", "two-bedroom"
            for word, num in word_numbers.items():
                pattern = rf'{word}[\s-]*{keyword}'
                if re.search(pattern, text):
                    return num
        
        return 1
    
    def _generate_structure(self):
        """Generate walls, rooms, and openings based on parsed requirements."""
        rooms = self._rooms_to_create
        
        # Calculate total area if not specified
        if self.schema.house.total_area_m2 == 0:
            # Estimate: ~15-20 m2 per room
            self.schema.house.total_area_m2 = len(rooms) * 18
        
        # Calculate footprint dimensions (assume rectangular)
        area = self.schema.house.total_area_m2
        aspect_ratio = 1.3  # Slightly longer than wide
        self.schema.house.width_m = (area / aspect_ratio) ** 0.5
        self.schema.house.depth_m = area / self.schema.house.width_m
        self.schema.house.footprint_shape = "rectangle"
        
        # Generate rooms with bounds
        current_x = 0.0
        wall_thickness = 0.2
        
        for i, (room_type, room_id) in enumerate(rooms):
            # Calculate room dimensions
            room_area = area / len(rooms)
            room_width = self.schema.house.width_m
            room_depth = room_area / room_width
            
            room = Room(
                room_id=room_id,
                name=room_type.capitalize().replace("_", " "),
                level_id="ground_floor",
                area_m2=room_area,
                shape="rectangle",
                bounds=RoomBounds(
                    x=current_x,
                    y=0.0,
                    width=room_width,
                    depth=room_depth
                ),
                room_type=room_type,
                privacy_level=self._get_privacy_level(room_type)
            )
            
            # Set adjacent rooms
            if i > 0:
                room.adjacent_rooms.append(rooms[i-1][1])
            if i < len(rooms) - 1:
                room.adjacent_rooms.append(rooms[i+1][1])
            
            self.schema.rooms.append(room)
            current_x += room_width
        
        # Generate exterior walls
        self._generate_exterior_walls()
        
        # Generate interior walls between rooms
        self._generate_interior_walls()
        
        # Generate openings (doors and windows)
        self._generate_openings()
        
        # Update confidence based on how well we matched the prompt
        self.schema.meta.confidence = 0.8 if len(rooms) > 1 else 0.6
    
    def _get_privacy_level(self, room_type: str) -> str:
        """Determine privacy level for room type."""
        if room_type == "bathroom" or room_type == "bedroom":
            return "private"
        elif room_type == "kitchen":
            return "semi-private"
        else:
            return "public"
    
    def _generate_exterior_walls(self):
        """Generate walls that enclose the building footprint."""
        w = self.schema.house.width_m
        d = self.schema.house.depth_m
        h = self.schema.house.ceiling_height_m
        t = 0.2
        
        # Four exterior walls forming a rectangle
        walls = [
            Wall("wall_ext_1", [0, 0], [w, 0], h, t, "ground_floor", True),
            Wall("wall_ext_2", [w, 0], [w, d], h, t, "ground_floor", True),
            Wall("wall_ext_3", [w, d], [0, d], h, t, "ground_floor", True),
            Wall("wall_ext_4", [0, d], [0, 0], h, t, "ground_floor", True),
        ]
        
        self.schema.walls.extend(walls)
    
    def _generate_interior_walls(self):
        """Generate walls separating rooms."""
        if len(self.schema.rooms) < 2:
            return
        
        h = self.schema.house.ceiling_height_m
        t = 0.15  # Interior walls thinner
        
        for i in range(len(self.schema.rooms) - 1):
            room1 = self.schema.rooms[i]
            room2 = self.schema.rooms[i + 1]
            
            # Wall at the boundary between rooms
            x_pos = room1.bounds.x + room1.bounds.width
            wall = Wall(
                f"wall_int_{i+1}",
                [x_pos, 0],
                [x_pos, room1.bounds.depth],
                h, t, "ground_floor", False
            )
            self.schema.walls.append(wall)
    
    def _generate_openings(self):
        """Generate doors and windows based on room requirements."""
        wall_id_counter = 1
        
        for room in self.schema.rooms:
            # Every room needs at least one door
            # Find a wall adjacent to this room
            wall_id = f"wall_int_{wall_id_counter}" if wall_id_counter <= len(self.schema.rooms) - 1 else "wall_ext_1"
            
            door = Opening(
                opening_id=f"door_{room.room_id}",
                type="door",
                wall_id=wall_id,
                position_ratio=0.5,
                width_m=0.9,
                height_m=2.1,
                swing="left",
                transparent=False
            )
            self.schema.openings.append(door)
            
            # Bedrooms require windows
            if room.room_type == "bedroom":
                window = Opening(
                    opening_id=f"window_{room.room_id}",
                    type="window",
                    wall_id="wall_ext_2",
                    position_ratio=0.5,
                    width_m=1.2,
                    height_m=1.5,
                    swing="none",
                    transparent=True
                )
                self.schema.openings.append(window)
            
            # Kitchens need ventilation (window)
            if room.room_type == "kitchen":
                window = Opening(
                    opening_id=f"window_{room.room_id}",
                    type="window",
                    wall_id="wall_ext_2",
                    position_ratio=0.3,
                    width_m=0.8,
                    height_m=1.2,
                    swing="none",
                    transparent=True
                )
                self.schema.openings.append(window)
            
            wall_id_counter += 1
    
    def _add_furniture(self):
        """Add appropriate furniture to each room based on type."""
        furniture_presets = {
            "bedroom": [
                ("bed", "modern_bed_01", [1.5, 2.0]),
                ("wardrobe", "wardrobe_modern_01", [0.5, 1.0]),
            ],
            "kitchen": [
                ("kitchen_cabinet", "kitchen_cabinet_modern_01", [2.0, 0.5]),
                ("refrigerator", "fridge_standard_01", [0.5, 0.6]),
            ],
            "living": [
                ("sofa", "modern_sofa_01", [2.0, 1.0]),
                ("coffee_table", "coffee_table_modern_01", [1.5, 0.8]),
            ],
            "bathroom": [
                ("toilet", "toilet_standard_01", [0.5, 0.4]),
                ("sink", "sink_modern_01", [1.0, 0.5]),
            ]
        }
        
        for room in self.schema.rooms:
            room_type = room.room_type
            if room_type in furniture_presets:
                for idx, (furn_type, preset, pos) in enumerate(furniture_presets[room_type]):
                    furniture = Furniture(
                        furniture_id=f"{furn_type}_{room.room_id}",
                        type=furn_type,
                        room_id=room.room_id,
                        position=[
                            pos[0],  # Store relative to room origin, not absolute
                            pos[1]   # Store relative to room origin, not absolute
                        ],
                        rotation_deg=0.0,
                        scale=1.0,
                        preset=preset
                    )
                    self.schema.furniture.append(furniture)
    
    def _apply_materials(self):
        """Apply default materials based on room types and style."""
        self.schema.materials = {
            "walls": "paint_white_matte",
            "floor_living": "wood_oak_light",
            "floor_bedroom": "wood_oak_light",
            "floor_kitchen": "tile_ceramic_gray",
            "floor_bathroom": "tile_ceramic_gray"
        }
        
        # Adjust based on style theme
        if self.schema.styles.theme == "scandinavian":
            self.schema.materials["walls"] = "paint_white_matte"
            self.schema.materials["floor_living"] = "wood_oak_light"
        elif self.schema.styles.theme == "industrial":
            self.schema.materials["walls"] = "concrete_exposed"
            self.schema.materials["floor_living"] = "concrete_polished"
        elif self.schema.styles.theme == "rustic":
            self.schema.materials["walls"] = "wood_panel_natural"
            self.schema.materials["floor_living"] = "wood_dark_oak"
