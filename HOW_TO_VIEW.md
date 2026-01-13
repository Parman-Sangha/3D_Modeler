# How to View Your 3D Scenes

## 🎯 Quick Start

### Option 1: View Existing Scene (Easiest)
```bash
python3 view_scene.py demo_scene.json
```

### Option 2: Generate & View New Scene
```bash
# Step 1: Generate a scene
python3 cli.py "A modern 2-bedroom apartment" -o my_scene.json

# Step 2: View it
python3 view_scene.py my_scene.json
```

### Option 3: View JSON Directly
```bash
# Pretty-printed JSON
cat demo_scene.json | python3 -m json.tool

# Or just view the file
cat demo_scene.json
```

## 📋 Step-by-Step Examples

### Example 1: View the Demo Scene
```bash
cd /Users/parmansangha/3D_Modeler
python3 view_scene.py demo_scene.json
```

**Output:** You'll see a formatted view showing:
- Room layouts and dimensions
- Wall structure
- Doors and windows
- Furniture placement
- Materials and styles

### Example 2: Create and View a New Scene
```bash
# Generate a Scandinavian apartment
python3 cli.py "A scandinavian 1-bedroom apartment" -o scandi_apt.json

# View it
python3 view_scene.py scandi_apt.json
```

### Example 3: Quick Preview (JSON Only)
```bash
# Generate and see JSON immediately
python3 cli.py "A modern apartment" --pretty
```

## 🛠️ Available Commands

### Generate Scenes
```bash
python3 cli.py "your description here" [options]

Options:
  --pretty          Pretty-print JSON
  -o filename.json  Save to file
  --validate        Validate output
```

### View Scenes
```bash
python3 view_scene.py filename.json
```

### Run Examples
```bash
python3 example.py          # See example outputs
python3 test_modeler.py     # Run tests
```

## 📁 Your Scene Files

Check what scenes you have:
```bash
ls -lh *.json
```

Current files:
- `demo_scene.json` - Industrial loft example
- `my_scene.json` - Another example

## 🎨 Try These Examples

```bash
# 1. Modern apartment
python3 cli.py "A modern 2-bedroom apartment" -o scene1.json
python3 view_scene.py scene1.json

# 2. Scandinavian style
python3 cli.py "A scandinavian studio" -o scene2.json
python3 view_scene.py scene2.json

# 3. Large house
python3 cli.py "A 3-bedroom house with 2 bathrooms and kitchen" -o scene3.json
python3 view_scene.py scene3.json
```

## 💡 Tips

1. **Always save to file** if you want to view it later:
   ```bash
   python3 cli.py "description" -o scene.json
   ```

2. **Use --pretty** for readable JSON in terminal:
   ```bash
   python3 cli.py "description" --pretty
   ```

3. **Use the viewer** for the best formatted output:
   ```bash
   python3 view_scene.py scene.json
   ```

## 🔍 What You'll See

The viewer shows:
- ✅ Room layouts with exact dimensions
- ✅ Wall positions and types
- ✅ Door and window placements
- ✅ Furniture locations
- ✅ Material assignments
- ✅ Style theme
- ✅ Export settings

## ❓ Troubleshooting

**"File not found" error?**
- Make sure you generated the scene first with `-o filename.json`
- Check the file exists: `ls *.json`

**Want to see raw JSON?**
- Use `cat filename.json`
- Or `python3 cli.py "description" --pretty`

**Want a quick summary?**
- The viewer script shows everything in a formatted way
- Just run: `python3 view_scene.py your_file.json`
