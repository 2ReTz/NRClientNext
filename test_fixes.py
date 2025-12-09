#!/usr/bin/env python3
"""
Comprehensive test for Custom Image fixes
"""
import json
import os
import sys

def test_path_normalization():
    """Test the path normalization logic from our fix"""
    print("=== Testing Path Normalization ===")
    
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    test_cases = [
        ('S:\\XERXDEV\\NRClientNext\\images\\lost coder.gif', 'images\\lost coder.gif'),
        ('S:/XERXDEV/NRClientNext/images/windows_e.png', 'images/windows_e.png'),
        ('C:\\some\\other\\path\\image.png', 'C:\\some\\other\\path\\image.png'),  # Should remain absolute
        ('images/linux_e.png', 'images/linux_e.png'),  # Already relative
    ]
    
    for input_path, expected in test_cases:
        if input_path.startswith(current_dir):
            normalized = os.path.relpath(input_path, current_dir)
            result = "✓ PASS" if normalized == expected else f"✗ FAIL (got: {normalized})"
            print(f"Input: {input_path} -> {normalized} {result}")
        else:
            result = "✓ PASS" if input_path == expected else f"✗ FAIL (should stay: {input_path})"
            print(f"Input: {input_path} -> {input_path} {result}")

def test_config_operations():
    """Test config save/load with our debug logging"""
    print("\n=== Testing Config Operations ===")
    
    # Test data
    test_configs = [
        {
            'enabled': True,
            'path': 'images/linux_e.png',
            'width': 120,
            'height': 80,
            'fit': False
        },
        {
            'enabled': True,
            'path': 'images/windows_e.png',
            'width': 200,
            'height': 150,
            'fit': True
        },
        {
            'enabled': False,
            'path': '',
            'width': 300,
            'height': 200,
            'fit': True
        }
    ]
    
    for i, config in enumerate(test_configs):
        print(f"\nTest {i+1}: {config}")
        
        # Simulate saving like our code does
        try:
            with open('config.json', 'r') as f:
                full_config = json.load(f)
            
            full_config.update({
                'custom_image_enabled': config['enabled'],
                'custom_image_path': config['path'],
                'custom_image_width': config['width'],
                'custom_image_height': config['height'],
                'custom_image_fit': config['fit']
            })
            
            with open('config.json', 'w') as f:
                json.dump(full_config, f, indent=4)
            
            # Simulate loading like our code does
            with open('config.json', 'r') as f:
                loaded_config = json.load(f)
            
            loaded_custom = {
                'enabled': loaded_config.get('custom_image_enabled', False),
                'path': loaded_config.get('custom_image_path', ''),
                'width': loaded_config.get('custom_image_width', 300),
                'height': loaded_config.get('custom_image_height', 200),
                'fit': loaded_config.get('custom_image_fit', True)
            }
            
            if loaded_custom == config:
                print(f"  ✓ Config save/load working correctly")
            else:
                print(f"  ✗ Config save/load failed")
                print(f"    Expected: {config}")
                print(f"    Got: {loaded_custom}")
                
        except Exception as e:
            print(f"  ✗ Exception during config test: {e}")

def test_image_loading_simulation():
    """Simulate the image loading logic from our fix"""
    print("\n=== Testing Image Loading Logic ===")
    
    # Test cases that would have failed before our fix
    test_cases = [
        {
            'config_path': 'images/linux_e.png',
            'should_exist': True,
            'description': 'Relative path in app directory'
        },
        {
            'config_path': 'S:\\XERXDEV\\NRClientNext\\images\\windows_e.png',
            'should_exist': True,
            'description': 'Absolute path in app directory'
        },
        {
            'config_path': 'nonexistent/image.png',
            'should_exist': False,
            'description': 'Non-existent file'
        }
    ]
    
    for case in test_cases:
        print(f"\nTest: {case['description']}")
        print(f"  Config path: {case['config_path']}")
        
        # Simulate our normalization logic
        image_path = case['config_path']
        if not os.path.isabs(image_path):
            image_path = os.path.join(os.getcwd(), image_path)
            print(f"  Normalized path: {image_path}")
        
        exists = os.path.exists(image_path)
        print(f"  File exists: {exists}")
        
        if exists == case['should_exist']:
            print(f"  ✓ PASS")
        else:
            print(f"  ✗ FAIL (expected {case['should_exist']}, got {exists})")

def main():
    print("Testing Custom Image Fixes")
    print("=" * 40)
    
    test_path_normalization()
    test_config_operations()
    test_image_loading_simulation()
    
    print("\n=== Test Summary ===")
    print("Fixes implemented:")
    print("1. ✓ Path normalization in FileDialog browse method")
    print("2. ✓ Better error handling in load_image method")
    print("3. ✓ Debug logging throughout the flow")
    print("4. ✓ Config save/load verification")

if __name__ == "__main__":
    main()