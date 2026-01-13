# 3D Modeler Pro 🏗️

**Text-to-3D Architectural Design & Interior Modeling Engine**

3D Modeler Pro converts natural-language architectural descriptions into structured JSON that serves as the single source of truth for 3D geometry generation, floorplans, furniture placement, and export pipelines.

## Features

- 🏠 **Residential Architecture**: Generate complete floorplans from text descriptions
- 🎨 **Style Detection**: Automatically applies themes (Scandinavian, Industrial, Modern, etc.)
- 📐 **Architectural Logic**: Enforces building codes and spatial relationships
- 🪑 **Furniture Placement**: Rule-based furniture arrangement by room type
- 📦 **Export Ready**: JSON compatible with Blender, Three.js, GLB/FBX/USDZ
- 🔧 **CLI & API**: Use from command line or import as Python module

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/3D_Modeler.git
cd 3D_Modeler
```

No external dependencies required for basic functionality!

### Command Line Usage

```bash
# Generate JSON from description
python3 cli.py "A 2-bedroom apartment with modern kitchen" --pretty

# Save to file
python3 cli.py "Scandinavian 1-bedroom, 60 square meters" -o scene.json

# Validate output
python3 cli.py "Industrial loft" --validate
```

### Python API

```python
from modeler import ModelerPro

modeler = ModelerPro()
json_output = modeler.generate("A 2-bedroom apartment with modern kitchen")
print(json_output)
```

### Example Output

```json
{
  "meta": {
    "version": "1.0",
    "unit_system": "metric",
    "generated_by": "3D Modeler Pro",
    "confidence": 0.8
  },
  "house": {
    "type": "residential",
    "footprint_shape": "rectangle",
    "total_area_m2": 36,
    "ceiling_height_m": 2.7
  },
  "rooms": [...],
  "walls": [...],
  "openings": [...],
  "furniture": [...]
}
```

## Architecture

- **`schema.py`**: Type-safe data structures and JSON schema definitions
- **`modeler.py`**: Core architectural reasoning and generation engine
- **`cli.py`**: Command-line interface
- **`test_modeler.py`**: Test suite for validation

## Supported Features

### Room Types
- Bedrooms (with windows)
- Bathrooms (with doors)
- Kitchens (with ventilation)
- Living rooms
- Hallways
- Storage

### Style Themes
- Scandinavian
- Industrial
- Minimalist
- Modern
- Rustic

### Architectural Rules
- Closed wall loops
- Proper room adjacencies
- Required openings (doors/windows)
- Walking clearance for furniture
- Privacy levels

## Testing

Run the test suite:

```bash
python3 test_modeler.py
```

## Output Format

All outputs are valid JSON following a strict schema with these required keys:
- `meta`: Version, confidence, generation metadata
- `house`: Overall building properties
- `levels`: Multi-floor support
- `rooms`: Room definitions with bounds
- `walls`: Structural walls
- `openings`: Doors and windows
- `furniture`: Placed furniture items
- `materials`: Material assignments
- `styles`: Design theme
- `constraints`: Accessibility, budget, region
- `exports`: Export configuration

## Roadmap

- [ ] Image-to-3D (blueprint parsing)
- [ ] Multi-floor support
- [ ] Advanced furniture presets
- [ ] Blender integration script
- [ ] Three.js viewer
- [ ] AR/VR export formats

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
