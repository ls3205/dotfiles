#!/usr/bin/env python3
# filepath: c:\Users\leons\.config\scripts\UpdateYasbColors.py
import os
import json
import re
import shutil
import sys
from pathlib import Path

def find_winwal_colors():
    """Find and load the winwal colors file with proper escape handling"""
    home_dir = os.path.expanduser("~")
    # First try the primary location specified by user
    primary_path = os.path.join(home_dir, ".cache", "wal", "colors.json")
    
    if os.path.exists(primary_path):
        try:
            # Read the file contents as a string first
            with open(primary_path, 'r') as f:
                json_content = f.read()
            
            # Fix common issues with escape sequences
            json_content = json_content.replace('\\', '\\\\')  # Double all backslashes
            json_content = json_content.replace('\\\\\"', '\\"')  # Fix any already escaped quotes
            json_content = json_content.replace('\\\\n', '\\n')  # Fix any already escaped newlines
            
            # Parse the fixed JSON content
            wal_data = json.loads(json_content)
            print(f"Found winwal colors at: {primary_path}")
            return wal_data
            
        except Exception as e:
            print(f"Error parsing colors file at {primary_path}: {e}")
    else:
        print(f"Primary colors path not found: {primary_path}")
    
    # Fallback to other possible locations
    fallback_paths = [
        os.path.join(home_dir, "AppData", "Local", "winwal", "colors.json"),
        os.path.join(home_dir, "AppData", "Roaming", "winwal", "colors.json"),
        os.path.join(home_dir, ".config", "winwal", "colors.json"),
    ]
    
    for path in fallback_paths:
        if os.path.exists(path):
            try:
                # Read file contents and fix escapes
                with open(path, 'r') as f:
                    json_content = f.read()
                
                # Fix common issues with escape sequences
                json_content = json_content.replace('\\', '\\\\')
                json_content = json_content.replace('\\\\\"', '\\"')
                json_content = json_content.replace('\\\\n', '\\n')
                
                wal_data = json.loads(json_content)
                print(f"Found winwal colors at: {path}")
                return wal_data
                
            except Exception as e:
                print(f"Error with fallback path {path}: {e}")
                continue
    
    print("Could not find winwal colors file automatically.")
    print("Please enter the full path to your winwal colors.json file:")
    user_path = input("> ").strip()
    
    if not user_path:
        print("No path provided. Exiting.")
        sys.exit(1)
        
    try:
        # Read file with escape handling
        with open(user_path, 'r') as f:
            json_content = f.read()
        
        # Fix common issues with escape sequences
        json_content = json_content.replace('\\', '\\\\')
        json_content = json_content.replace('\\\\\"', '\\"')
        json_content = json_content.replace('\\\\n', '\\n')
        
        return json.loads(json_content)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def backup_css(css_path):
    """Create a backup of the CSS file"""
    backup_path = f"{css_path}.bak"
    try:
        shutil.copy2(css_path, backup_path)
        print(f"Created backup at: {backup_path}")
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")

def extract_colors(winwal_data):
    """Extract colors from winwal data in various possible formats"""
    colors = {}
    
    # Handle pywal format with nested structure
    if isinstance(winwal_data, dict):
        if "colors" in winwal_data and isinstance(winwal_data["colors"], dict):
            for i in range(16):
                color_key = f"color{i}"
                if color_key in winwal_data["colors"]:
                    colors[color_key] = winwal_data["colors"][color_key]
        
        if "special" in winwal_data and isinstance(winwal_data["special"], dict):
            for key in ["background", "foreground", "cursor"]:
                if key in winwal_data["special"]:
                    colors[key] = winwal_data["special"][key]
        
        # Handle flat format
        for key in ["color0", "color1", "color2", "color3", "color4", "color5", 
                   "color6", "color7", "color8", "color9", "color10", "color11", 
                   "color12", "color13", "color14", "color15", 
                   "background", "foreground", "cursor"]:
            if key in winwal_data and key not in colors:
                colors[key] = winwal_data[key]
    
    return colors

def update_css_property(css_content, selector, property_name, new_value):
    """Update a specific CSS property for a selector"""
    pattern = rf'({re.escape(selector)}\s*{{[^}}]*?{re.escape(property_name)}:\s*)#[0-9a-fA-F]{{6}}([^}}]*?}})'
    replacement = rf'\g<1>{new_value}\g<2>'
    return re.sub(pattern, replacement, css_content, flags=re.DOTALL)

def update_yasb_css(css_path, colors):
    """Update the YASB CSS with the new colors"""
    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
    except Exception as e:
        print(f"Error reading CSS file: {e}")
        sys.exit(1)
    
    # Map winwal colors to yasb elements
    main_bg = colors.get("background", "#221f2e")
    main_fg = colors.get("foreground", "#bec8e7")
    accent1 = colors.get("color4", "#c2a8e3")  # Purple
    accent2 = colors.get("color6", "#9ecfd7")  # Cyan
    accent3 = colors.get("color1", "#f38ba8")  # Red
    accent4 = colors.get("color3", "#f5c276")  # Yellow
    
    # Define color mappings - selector: {property: color}
    mappings = {
        # General
        "*": {"color": main_fg},
        ".komorebi-workspaces": {"background-color": main_bg},
        ".taskbar-widget": {"background-color": main_bg},
        
        # Workspaces
        ".komorebi-workspaces .ws-btn": {"background-color": colors.get("color7", "#9cd1dd")},
        ".komorebi-workspaces .ws-btn.populated": {"background-color": accent3},
        ".komorebi-workspaces .ws-btn.active": {"background-color": accent1},
        
        # Widgets
        ".clock-widget": {"background-color": accent1},
        ".weather-widget": {"background-color": accent2},
        ".volume-widget": {"background-color": accent3},
        ".power-menu-widget": {"background-color": accent1},
        ".language-widget": {"background-color": accent4},
        ".traffic-widget": {"background-color": accent2},
        ".active-window-widget": {"background-color": accent1},
        
        # Widget labels
        ".clock-widget .label": {"color": accent1, "background-color": main_bg},
        ".weather-widget .label": {"color": accent2, "background-color": main_bg},
        ".volume-widget .label": {"color": accent3, "background-color": main_bg},
        ".language-widget .label": {"color": accent4, "background-color": main_bg},
        ".traffic-widget .label": {"color": accent2, "background-color": main_bg},
        ".active-window-widget .label": {"color": accent1, "background-color": main_bg},
        
        # Widget icons
        ".clock-widget .icon": {"color": main_bg},
        ".weather-widget .icon": {"color": main_bg},
        ".volume-widget .icon": {"color": main_bg},
        ".language-widget .icon": {"color": main_bg},
        ".traffic-widget .icon": {"color": main_bg},
        ".power-menu-widget .label": {"color": main_bg},
        ".win-btn .icon": {"color": main_bg},
        
        # Power menu
        ".power-menu-popup .button": {"background-color": main_bg, "color": accent1},
        ".power-menu-popup .button.hover": {"background-color": colors.get("color0", "#1b1925")},
        ".power-menu-popup .button .label": {"color": accent1},
        ".power-menu-popup .button .icon": {"color": accent1},
    }
    
    # Apply the color mappings
    for selector, properties in mappings.items():
        for prop, value in properties.items():
            css_content = update_css_property(css_content, selector, prop, value)
    
    # Write the updated CSS
    try:
        with open(css_path, 'w') as f:
            f.write(css_content)
        print(f"Successfully updated CSS file: {css_path}")
    except Exception as e:
        print(f"Error writing to CSS file: {e}")
        sys.exit(1)

def main():
    yasb_css_path = os.path.join(os.path.expanduser("~"), ".config", "yasb", "styles.css")
    
    print("Updating YASB colors with winwal theme...")
    print("Looking for colors in ~/.cache/wal/...")
    winwal_data = find_winwal_colors()
    colors = extract_colors(winwal_data)
    
    if not colors:
        print("Error: Could not extract colors from winwal data")
        sys.exit(1)
    
    print(f"Found {len(colors)} colors in the winwal theme")
    backup_css(yasb_css_path)
    update_yasb_css(yasb_css_path, colors)
    print("Done! Restart YASB to see the changes.")

if __name__ == "__main__":
    main()