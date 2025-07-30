#!/usr/bin/env python3

import json
import os
import shutil
import re
from pathlib import Path

def main():
    # Use Path for better path handling
    home_dir = Path.home()
    komorebi_config_path = home_dir / ".config" / "komorebi" / "komorebi.json" 
    wal_colors_path = home_dir / ".cache" / "wal" / "colors.json"
    
    # Check if files exist
    if not wal_colors_path.exists():
        print(f"Error: winwal colors file not found at {wal_colors_path}")
        return 1
    
    if not komorebi_config_path.exists():
        print(f"Error: Komorebi config file not found at {komorebi_config_path}")
        return 1
    
    # Create backup of the original config
    backup_path = komorebi_config_path.with_suffix('.json.bak')
    shutil.copy2(komorebi_config_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Load Komorebi config
    try:
        # Read the raw content first
        with open(komorebi_config_path, 'r') as f:
            lines = f.readlines()
        
        # Filter out comment lines and create a clean JSON
        clean_lines = []
        for line in lines:
            if not line.strip().startswith('//'):
                clean_lines.append(line)
        
        clean_json = ''.join(clean_lines)
        komorebi_config = json.loads(clean_json)
        
    except Exception as e:
        print(f"Error loading komorebi config: {e}")
        return 1
    
    # Load winwal colors with extra care for potentially malformed JSON
    colors = {}
    try:
        # Read raw content
        with open(wal_colors_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix any potential issues with escape characters
        # Replace any problematic escape sequences
        content = content.replace('\\', '\\\\')  # Double escape backslashes
        content = re.sub(r'\\(?!["\\/bfnrt])', r'\\\\', content)  # Escape invalid escapes
        
        # Try to parse the JSON
        wal_data = json.loads(content)
        colors = wal_data.get('colors', {})
        
    except json.JSONDecodeError as e:
        print(f"Error parsing winwal colors.json: {e}")
        print("Attempting to read colors directly from file...")
        
        # Fallback: try to extract colors using regex
        try:
            with open(wal_colors_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract colors using regex
            color_pattern = r'"color(\d+)"\s*:\s*"(#[0-9a-fA-F]+)"'
            matches = re.findall(color_pattern, content)
            
            for num, color in matches:
                colors[f'color{num}'] = color
                
            # Look for background/foreground
            bg_match = re.search(r'"background"\s*:\s*"(#[0-9a-fA-F]+)"', content)
            if bg_match:
                colors['color0'] = bg_match.group(1)
            
            if not colors:
                print("Could not extract colors from malformed JSON.")
                return 1
                
        except Exception as e2:
            print(f"Failed to extract colors: {e2}")
            return 1
    
    # Map winwal colors to komorebi border colors
    if colors:
        print("Updating Komorebi border colors:")
        print(f"  Monocle: {colors.get('color1', '#f38ba8')}")
        print(f"  Single: {colors.get('color4', '#89b4fa')}")
        print(f"  Stack: {colors.get('color2', '#a6e3a1')}")
        print(f"  Unfocused: {colors.get('color0', '#10151D')}")
        
        komorebi_config['border_colours'] = {
            "monocle": colors.get('color1', "#f38ba8"),    # Red/pink tone
            "single": colors.get('color4', "#89b4fa"),     # Blue tone
            "stack": colors.get('color2', "#a6e3a1"),      # Green tone
            "unfocused": colors.get('color0', "#10151D")   # Dark/background color
        }
    else:
        print("No colors found in winwal file. Using defaults.")
    
    # Write updated config
    try:
        with open(komorebi_config_path, 'w') as f:
            # Preserve the schema comment if it existed in the original file
            schema_pattern = r'//\s*\$schema'
            if any(re.search(schema_pattern, line) for line in lines):
                f.write('// $schema: "https://raw.githubusercontent.com/LGUG2Z/komorebi/v0.1.34/schema.json"\n')
            
            json.dump(komorebi_config, f, indent=2)
            
        print(f"Successfully updated komorebi colors from winwal!")
    except Exception as e:
        print(f"Error writing updated config: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())