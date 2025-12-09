#!/usr/bin/env python3
"""
Debug script to test Custom Image functionality
"""
import json
import os
import sys

# Test the config loading/saving logic
def test_config_operations():
    print("=== Testing Config Operations ===")
    
    # Read current config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(f"Current config: {config}")
    except Exception as e:
        print(f"Error reading config: {e}")
        return
    
    # Test updating config
    original_config = config.copy()
    config.update({
        'custom_image_enabled': True,
        'custom_image_path': 'images/windows_e.png',
        'custom_image_width': 200,
        'custom_image_height': 150,
        'custom_image_fit': True
    })
    
    print(f"Updated config: {config}")
    
    # Save config
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print("Config saved successfully")
    except Exception as e:
        print(f"Error saving config: {e}")
        return
    
    # Verify saved config
    try:
        with open('config.json', 'r') as f:
            saved_config = json.load(f)
        print(f"Saved config verification: {saved_config}")
        
        # Check if changes were applied
        if saved_config == config:
            print("✓ Config save/load working correctly")
        else:
            print("✗ Config save/load mismatch")
            print(f"Expected: {config}")
            print(f"Got: {saved_config}")
    except Exception as e:
        print(f"Error verifying saved config: {e}")
    
    # Restore original config
    try:
        with open('config.json', 'w') as f:
            json.dump(original_config, f, indent=4)
        print("Original config restored")
    except Exception as e:
        print(f"Error restoring config: {e}")

# Test image file existence and accessibility
def test_image_files():
    print("\n=== Testing Image Files ===")
    
    test_images = [
        'images/linux_e.png',
        'images/windows_e.png',
        'images/lost coder.gif'
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            print(f"✓ {img_path} exists ({size} bytes)")
        else:
            print(f"✗ {img_path} not found")

# Test path handling issues
def test_path_handling():
    print("\n=== Testing Path Handling ===")
    
    # Test different path formats
    test_paths = [
        'images/linux_e.png',  # Relative path
        './images/linux_e.png',  # Relative with ./
        'S:\\XERXDEV\\NRClientNext\\images\\linux_e.png',  # Absolute Windows path
    ]
    
    for path in test_paths:
        exists = os.path.exists(path)
        print(f"Path '{path}': {'✓ exists' if exists else '✗ not found'}")

if __name__ == "__main__":
    test_config_operations()
    test_image_files()
    test_path_handling()
    print("\n=== Test Complete ===")