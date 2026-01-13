"""
Example usage of 3D Modeler Pro
"""

from modeler import ModelerPro

def main():
    modeler = ModelerPro()
    
    # Example 1: Simple apartment
    prompt1 = "A 2-bedroom apartment with modern kitchen"
    result1 = modeler.generate(prompt1)
    print("Example 1: 2-bedroom apartment")
    print(result1)
    print("\n" + "="*80 + "\n")
    
    # Example 2: Scandinavian style
    prompt2 = "A scandinavian 1-bedroom apartment, 60 square meters"
    result2 = modeler.generate(prompt2)
    print("Example 2: Scandinavian apartment")
    print(result2)
    print("\n" + "="*80 + "\n")
    
    # Example 3: Industrial loft
    prompt3 = "An industrial loft with living room and bathroom"
    result3 = modeler.generate(prompt3)
    print("Example 3: Industrial loft")
    print(result3)

if __name__ == "__main__":
    main()
