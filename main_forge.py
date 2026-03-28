import argparse
import os
import sys
import json
from forge.generator import generate_bpy_script
from forge.packager import prepare_package_dir, write_manifest
from blender.headless import execute_headless_blender

def main():
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - OBJ Baseline Pipeline")
    parser.add_argument("-f", "--file", type=str, help="Path to a JSON request file")
    parser.add_argument("--name", type=str, help="Asset name")
    parser.add_argument("--primitive", type=str, choices=["cube", "sphere", "cylinder", "plane"], help="Primitive type")
    parser.add_argument("--scale", type=str, help="Comma-separated scale (x,y,z)")
    parser.add_argument("--output-dir", type=str, help="Output root directory")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--no-preview", action="store_true", default=None, help="Disable preview rendering")
    
    args = parser.parse_args()
    
    # Defaults (if neither CLI nor file provides them)
    name = "prop"
    primitive = "cube"
    scale_tuple = (1.0, 1.0, 1.0)
    output_dir = "outputs"
    tags_list = []
    no_preview = False

    # 1. Load from file if provided
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: Request file not found: {args.file}")
            sys.exit(1)
        
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
            
            asset_data = data.get("asset", {})
            options_data = data.get("options", {})
            
            # STRICT VALIDATION: Required fields in JSON
            missing_fields = []
            if "name" not in asset_data: missing_fields.append("asset.name")
            if "primitive" not in asset_data: missing_fields.append("asset.primitive")
            
            if missing_fields:
                print(f"Error: Missing required fields in request file: {', '.join(missing_fields)}")
                sys.exit(1)
                
            # Apply JSON values
            name = asset_data["name"]
            primitive = asset_data["primitive"]
            if "scale" in asset_data:
                scale_tuple = tuple(map(float, asset_data["scale"]))
            
            if "output_dir" in options_data:
                output_dir = options_data["output_dir"]
            if "tags" in options_data:
                tags_list = options_data["tags"]
            if "no_preview" in options_data:
                no_preview = options_data["no_preview"]
                
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse request file JSON: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Failed to process request file: {e}")
            sys.exit(1)

    # 2. CLI Overrides (Explicitly provided by user)
    # Note: We check if the user actually passed these flags via sys.argv or comparing to None
    if args.name is not None: name = args.name
    if args.primitive is not None: primitive = args.primitive
    if args.scale is not None:
        try:
            scale_tuple = tuple(map(float, args.scale.split(",")))
        except ValueError:
            print("Error: --scale must be three comma-separated numbers (e.g., 1.0,2.0,0.1)")
            sys.exit(1)
    if args.output_dir is not None: output_dir = args.output_dir
    if args.tags is not None:
        tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.no_preview is not None:
        no_preview = args.no_preview

    # Final validation for defaults if not using a file
    if not args.file:
        # Fallback to hardcoded defaults for name and primitive if not in CLI
        pass # Already handled by initialization above

    print(f"--- MStorm Asset Forge: START for '{name}' ---")
    
    # 3. Prepare Package Directory
    try:
        package_path = prepare_package_dir(output_dir, name)
        print(f"Forge: Created package directory: {package_path}")
    except Exception as e:
        print(f"Forge: CRITICAL ERROR - Package directory creation failed: {e}")
        sys.exit(1)
        
    # Standard internal asset names
    asset_file = "asset.obj"
    asset_path = os.path.join(package_path, asset_file)
    
    preview_file = "preview.png"
    preview_path = os.path.join(package_path, preview_file) if not no_preview else None
    
    # 4. Generate and Execute BPY script
    bpy_script = generate_bpy_script(
        name, primitive, scale_tuple, 
        output_path=asset_path, 
        preview_path=preview_path
    )
    
    print(f"Forge: Executing Blender headless (OBJ/MTL" + (" + Preview" if preview_path else "") + ")...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 5. Handle Result and Finalize Manifest
    if result.get("status") == "success":
        print(f"Forge: Blender execution SUCCESS.")
        
        # Check if preview actually exists
        final_preview = None
        if preview_path and os.path.exists(preview_path):
            final_preview = preview_file
            print(f"Forge: Preview rendered successfully.")
        elif preview_path:
            print(f"Forge: WARNING - Preview was requested but not found at {preview_path}.")
            
        # Write manifest last to reflect actual content
        manifest_path = write_manifest(
            package_path, name, primitive, scale_tuple, 
            tags=tags_list,
            preview_file=final_preview
        )
        print(f"Forge: Manifest written to {manifest_path}")
        
        print(f"Forge: Successfully packaged '{name}' in {package_path}")
        print(f"--- MStorm Asset Forge: DONE ---")
    else:
        print(f"Forge: Blender execution FAILED.")
        print(f"Error Message: {result.get('message')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
