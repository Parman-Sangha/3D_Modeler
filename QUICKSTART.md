# Quick Start Guide

## 🚀 Running the Project

### Method 1: Command Line Interface (Easiest)

```bash
# Basic usage - outputs JSON to terminal
python3 cli.py "A 2-bedroom apartment with modern kitchen"

# Pretty-printed JSON
python3 cli.py "Scandinavian 1-bedroom, 60 square meters" --pretty

# Save to file
python3 cli.py "Industrial loft" -o my_scene.json

# Validate output
python3 cli.py "A modern apartment" --validate
```

### Method 2: Python API

```python
from modeler import ModelerPro

# Create modeler instance
modeler = ModelerPro()

# Generate scene from description
json_output = modeler.generate("A 2-bedroom apartment with modern kitchen")
print(json_output)

# Parse the JSON
import json
scene = json.loads(json_output)
print(f"Created {len(scene['rooms'])} rooms")
print(f"Confidence: {scene['meta']['confidence']}")
```

### Method 3: Run Examples

```bash
# See example outputs
python3 example.py

# Run test suite
python3 test_modeler.py
```

## 📊 Viewing the Output

The output is **valid JSON** that you can:

1. **View in terminal** (with `--pretty` flag)
2. **Save to file** (with `-o filename.json`)
3. **Parse programmatically** (import as Python dict)
4. **Visualize** (use with Blender, Three.js, or other 3D tools)

## 🎨 Example Prompts

Try these:

```bash
# Simple apartment
python3 cli.py "A 1-bedroom apartment" --pretty

# Multiple rooms
python3 cli.py "A 3-bedroom house with 2 bathrooms and kitchen" --pretty

# Style themes
python3 cli.py "A scandinavian 2-bedroom apartment" --pretty
python3 cli.py "An industrial loft with living room" --pretty

# Specific size
python3 cli.py "A modern 1-bedroom apartment, 50 square meters" --pretty
```

## 📁 Output Structure

Each JSON output contains:
- `meta`: Version, confidence score
- `house`: Overall building properties
- `rooms`: Room definitions with dimensions
- `walls`: Structural walls
- `openings`: Doors and windows
- `furniture`: Placed furniture items
- `materials`: Material assignments
- `styles`: Design theme
- `constraints`: Accessibility, budget
- `exports`: Export configuration

## 🔍 Inspecting Output

```bash
# Save to file and view
python3 cli.py "A modern apartment" -o scene.json --pretty
cat scene.json | python3 -m json.tool  # Pretty print
cat scene.json | jq '.'  # If you have jq installed
```

## ✅ Testing

```bash
# Run all tests
python3 test_modeler.py

# Expected output: All tests should pass ✓
```

## 🎯 Next Steps

1. **Generate scenes** using the CLI
2. **Export JSON** to use with Blender or Three.js
3. **Modify the code** to add custom features
4. **Integrate** with 3D visualization tools
