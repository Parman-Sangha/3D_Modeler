#!/usr/bin/env python3
"""
Command-line interface for 3D Modeler Pro
"""

import sys
import json
import argparse
from modeler import ModelerPro


def main():
    parser = argparse.ArgumentParser(
        description="3D Modeler Pro - Text-to-3D Architectural Design Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A 2-bedroom apartment with modern kitchen"
  %(prog)s "Scandinavian 1-bedroom, 60 square meters" --output scene.json
  %(prog)s "Industrial loft" --pretty
        """
    )
    
    parser.add_argument(
        "prompt",
        help="Natural language description of the architectural space"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output (default: compact)"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate JSON output before saving"
    )
    
    args = parser.parse_args()
    
    # Generate scene
    try:
        modeler = ModelerPro()
        result = modeler.generate(args.prompt)
        
        # Parse to validate
        if args.validate:
            data = json.loads(result)
            print(f"✓ Valid JSON generated", file=sys.stderr)
            print(f"  - Rooms: {len(data['rooms'])}", file=sys.stderr)
            print(f"  - Confidence: {data['meta']['confidence']:.2f}", file=sys.stderr)
        
        # Format output
        if args.pretty:
            data = json.loads(result)
            result = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✓ Saved to {args.output}", file=sys.stderr)
        else:
            print(result)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
