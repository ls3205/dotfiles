#!/usr/bin/env python3
# filepath: UpdateGlazeColors.py

import json
import os
import shutil
import re
from pathlib import Path

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def main():
    # Get home directory
    home_dir = Path.home()
    
    # Define paths
    wal_colors_path = home_dir / ".cache" / "wal" / "colors.json"
    glazewm_config_path = home_dir / ".config" / "glazewm" / "config.yaml"
    zebar_css_path = home_dir / ".glzr" / "zebar" / "starter" / "styles.css"
    
    # Check if files exist
    if not wal_colors_path.exists():
        print(f"Error: pywal colors file not found at {wal_colors_path}")
        return
    
    if not glazewm_config_path.exists():
        print(f"Error: GlazeWM config file not found at {glazewm_config_path}")
        return
    
    if not zebar_css_path.exists():
        print(f"Error: Zebar CSS file not found at {zebar_css_path}")
        return
    
    # Load pywal colors with error handling
    try:
        # Read the file contents and fix any invalid escape sequences
        with open(wal_colors_path, 'r') as f:
            json_content = f.read()
            
        # Fix common issues with escape sequences
        json_content = json_content.replace('\\', '\\\\')  # Double all backslashes
        json_content = json_content.replace('\\\\\"', '\\"')  # Fix any already escaped quotes
        json_content = json_content.replace('\\\\n', '\\n')  # Fix any already escaped newlines
        
        # Parse the fixed JSON content
        wal_data = json.loads(json_content)
        
        # Extract colors
        colors = {
            'background': wal_data['special']['background'],
            'foreground': wal_data['special']['foreground'],
            'cursor': wal_data['special']['cursor'],
            'color0': wal_data['colors']['color0'],
            'color1': wal_data['colors']['color1'],
            'color2': wal_data['colors']['color2'],
            'color3': wal_data['colors']['color3'],
            'color4': wal_data['colors']['color4'],
            'color5': wal_data['colors']['color5'],
            'color6': wal_data['colors']['color6'],
            'color7': wal_data['colors']['color7'],
            'color8': wal_data['colors']['color8'],
            'color9': wal_data['colors']['color9'],
            'color10': wal_data['colors']['color10'],
            'color11': wal_data['colors']['color11'],
            'color12': wal_data['colors']['color12'],
            'color13': wal_data['colors']['color13'],
            'color14': wal_data['colors']['color14'],
            'color15': wal_data['colors']['color15'],
        }
        
    except json.JSONDecodeError as e:
        print(f"Error parsing colors.json: {e}")
        print("Trying alternative approach...")
        
        try:
            # Alternative approach: read colors directly from sequences file
            colors_file = home_dir / ".cache" / "wal" / "sequences"
            if colors_file.exists():
                with open(colors_file, 'r') as f:
                    sequences = f.read()
                
                # Extract colors from sequences (simplified fallback)
                color_matches = re.findall(r'\]10;(#[0-9A-Fa-f]{6})', sequences)
                if color_matches and len(color_matches) >= 2:
                    colors = {
                        'background': color_matches[0],
                        'foreground': color_matches[1],
                        'color4': color_matches[0],  # Use background as fallback
                        'color8': "#a1a1a1",  # Default gray
                    }
                else:
                    print("Could not extract sufficient colors from sequences file")
                    return
            else:
                print(f"Alternative colors file not found at {colors_file}")
                return
        except Exception as e:
            print(f"Error with alternative approach: {e}")
            return
    
    # Update GlazeWM config
    update_glazewm(glazewm_config_path, colors)
    
    # Update Zebar CSS
    update_zebar_css(zebar_css_path, colors)
    
    print("To apply changes, reload GlazeWM (alt+shift+r) and restart Zebar")

def update_glazewm(config_path, colors):
    """Update GlazeWM config colors"""
    # Create backup of GlazeWM config
    backup_path = config_path.with_suffix('.yaml.bak')
    shutil.copy2(config_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Extract specific colors for GlazeWM
    focused_color = colors.get('color4', '#0000FF')
    unfocused_color = colors.get('color8', '#A1A1A1')
    
    print(f"GlazeWM - Using colors:")
    print(f"  Focused window border: {focused_color}")
    print(f"  Unfocused window border: {unfocused_color}")
    
    # Read GlazeWM config
    with open(config_path, 'r') as f:
        glazewm_config = f.read()
    
    # Update the colors in the config using regex patterns
    # Update focused window border color
    glazewm_config = re.sub(
        r'(focused_window:\s*\n\s*# Highlight.*\n\s*border:\s*\n\s*enabled:.*\n\s*color:) .*',
        r'\1 "' + focused_color + '"',
        glazewm_config
    )
    
    # Update unfocused window border color
    glazewm_config = re.sub(
        r'(other_windows:\s*\n\s*border:\s*\n\s*enabled:.*\n\s*color:) .*',
        r'\1 "' + unfocused_color + '"',
        glazewm_config
    )
    
    # Write updated config
    with open(config_path, 'w') as f:
        f.write(glazewm_config)
    
    print(f"Updated GlazeWM config with pywal colors")

def update_zebar_css(css_path, colors):
    """Update Zebar CSS colors"""
    # Create backup of Zebar CSS
    backup_path = css_path.with_suffix('.css.bak')
    shutil.copy2(css_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Extract colors we want to use for Zebar
    accent_color_hex = colors.get('color4', '#4B73FF')  # Blue accent
    accent_rgb = hex_to_rgb(accent_color_hex)
    
    background_color_hex = colors.get('background', '#000000')  # Background
    background_rgb = hex_to_rgb(background_color_hex)
    
    foreground_color_hex = colors.get('foreground', '#FFFFFF')  # Foreground
    foreground_rgb = hex_to_rgb(foreground_color_hex)
    
    # Secondary background color - slightly lighter than background
    secondary_bg_hex = colors.get('color0', '#050214')  # Usually color0 is dark background
    secondary_bg_rgb = hex_to_rgb(secondary_bg_hex)
    
    print(f"Zebar - Using colors:")
    print(f"  Accent: {accent_color_hex} -> rgb({accent_rgb[0]}, {accent_rgb[1]}, {accent_rgb[2]})")
    print(f"  Background: {background_color_hex} -> rgb({background_rgb[0]}, {background_rgb[1]}, {background_rgb[2]})")
    print(f"  Foreground: {foreground_color_hex} -> rgb({foreground_rgb[0]}, {foreground_rgb[1]}, {foreground_rgb[2]})")
    
    # Read CSS file
    with open(css_path, 'r') as f:
        css_content = f.read()
    
    # Update icon color (using accent color)
    css_content = re.sub(
        r'i \{\s*color: rgb\([^)]+\);',
        f'i {{\n  color: rgb({accent_rgb[0]} {accent_rgb[1]} {accent_rgb[2]} / 95%);',
        css_content
    )
    
    # Update text color (using foreground color)
    css_content = re.sub(
        r'body \{\s*color: rgb\([^)]+\);',
        f'body {{\n  color: rgb({foreground_rgb[0]} {foreground_rgb[1]} {foreground_rgb[2]} / 90%);',
        css_content
    )
    
    # Update background gradient
    css_content = re.sub(
        r'background: linear-gradient\(rgb\([^)]+\), rgb\([^)]+\)\);',
        f'background: linear-gradient(rgb({background_rgb[0]} {background_rgb[1]} {background_rgb[2]} / 90%), ' +
        f'rgb({secondary_bg_rgb[0]} {secondary_bg_rgb[1]} {secondary_bg_rgb[2]} / 85%));',
        css_content
    )
    
    # Update focused workspace background (using accent color)
    css_content = re.sub(
        r'background: rgb\(75 115 255 \/ 50%\);',
        f'background: rgb({accent_rgb[0]} {accent_rgb[1]} {accent_rgb[2]} / 50%);',
        css_content
    )
    
    # Write updated CSS
    with open(css_path, 'w') as f:
        f.write(css_content)
    
    print(f"Updated Zebar CSS with pywal colors")

if __name__ == "__main__":
    main()
