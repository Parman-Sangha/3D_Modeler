"""
Test suite for 3D Modeler Pro
Validates JSON output structure and architectural logic.
"""

import json
from modeler import ModelerPro


def validate_json_structure(data: dict) -> tuple[bool, list[str]]:
    """Validate that JSON follows required schema."""
    errors = []
    required_keys = [
        "meta", "house", "levels", "rooms", "walls", "openings",
        "furniture", "materials", "styles", "constraints", "exports"
    ]
    
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    
    # Validate meta
    if "meta" in data:
        meta = data["meta"]
        if "version" not in meta or "confidence" not in meta:
            errors.append("Meta missing required fields")
    
    # Validate house
    if "house" in data:
        house = data["house"]
        if "total_area_m2" not in house or "width_m" not in house:
            errors.append("House missing required fields")
    
    return len(errors) == 0, errors


def test_basic_generation():
    """Test basic JSON generation."""
    modeler = ModelerPro()
    result = modeler.generate("A simple apartment")
    
    try:
        data = json.loads(result)
        valid, errors = validate_json_structure(data)
        
        if valid:
            print("✓ Basic generation: PASSED")
            print(f"  - Rooms: {len(data['rooms'])}")
            print(f"  - Walls: {len(data['walls'])}")
            print(f"  - Openings: {len(data['openings'])}")
            return True
        else:
            print(f"✗ Basic generation: FAILED - {errors}")
            return False
    except json.JSONDecodeError as e:
        print(f"✗ Basic generation: FAILED - Invalid JSON: {e}")
        return False


def test_multi_room():
    """Test multi-room detection."""
    modeler = ModelerPro()
    result = modeler.generate("A 3-bedroom house with 2 bathrooms")
    
    try:
        data = json.loads(result)
        bedrooms = [r for r in data['rooms'] if r['room_type'] == 'bedroom']
        bathrooms = [r for r in data['rooms'] if r['room_type'] == 'bathroom']
        
        if len(bedrooms) >= 3 and len(bathrooms) >= 2:
            print("✓ Multi-room detection: PASSED")
            print(f"  - Bedrooms: {len(bedrooms)}")
            print(f"  - Bathrooms: {len(bathrooms)}")
            return True
        else:
            print(f"✗ Multi-room detection: FAILED")
            print(f"  - Expected 3+ bedrooms, got {len(bedrooms)}")
            print(f"  - Expected 2+ bathrooms, got {len(bathrooms)}")
            return False
    except Exception as e:
        print(f"✗ Multi-room detection: FAILED - {e}")
        return False


def test_style_detection():
    """Test style theme detection."""
    modeler = ModelerPro()
    result = modeler.generate("A scandinavian apartment")
    
    try:
        data = json.loads(result)
        theme = data['styles']['theme']
        
        if theme == "scandinavian":
            print("✓ Style detection: PASSED")
            print(f"  - Theme: {theme}")
            return True
        else:
            print(f"✗ Style detection: FAILED - Expected 'scandinavian', got '{theme}'")
            return False
    except Exception as e:
        print(f"✗ Style detection: FAILED - {e}")
        return False


def test_architectural_rules():
    """Test that architectural rules are followed."""
    modeler = ModelerPro()
    result = modeler.generate("A bedroom with bathroom")
    
    try:
        data = json.loads(result)
        
        # Check that bedrooms have windows
        bedrooms = [r for r in data['rooms'] if r['room_type'] == 'bedroom']
        bedroom_windows = [
            o for o in data['openings']
            if o['type'] == 'window' and any(
                r['room_id'] in o['opening_id'] for r in bedrooms
            )
        ]
        
        # Check that bathrooms have doors
        bathrooms = [r for r in data['rooms'] if r['room_type'] == 'bathroom']
        bathroom_doors = [
            o for o in data['openings']
            if o['type'] == 'door' and any(
                r['room_id'] in o['opening_id'] for r in bathrooms
            )
        ]
        
        rules_passed = True
        if bedrooms and not bedroom_windows:
            print("  ⚠ Bedrooms should have windows")
            rules_passed = False
        if bathrooms and not bathroom_doors:
            print("  ⚠ Bathrooms should have doors")
            rules_passed = False
        
        if rules_passed:
            print("✓ Architectural rules: PASSED")
            return True
        else:
            print("✗ Architectural rules: FAILED")
            return False
    except Exception as e:
        print(f"✗ Architectural rules: FAILED - {e}")
        return False


if __name__ == "__main__":
    print("Running 3D Modeler Pro Test Suite\n")
    print("=" * 50)
    
    tests = [
        test_basic_generation,
        test_multi_room,
        test_style_detection,
        test_architectural_rules
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{len(tests)} tests passed")
