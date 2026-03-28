import argparse
import os
import sys
from forge.generator import generate_bpy_script
from forge.packager import prepare_package_dir, write_manifest
from blender.headless import execute_headless_blender

def main():
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - OBJ Baseline Pipeline")
    parser.add_argument("--name", type=str, default="prop", help="Asset name")
    parser.add_argument("--primitive", type=str, default="cube", choices=["cube", "sphere", "cylinder", "plane"], help="Primitive type")
    parser.add_argument("--scale", type=str, default="1.0,1.0,1.0", help="Comma-separated scale (x,y,z)")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output root directory")
    parser.add_argument("--tags", type=str, default="", help="Comma-separated tags")
    parser.add_argument("--no-preview", action="store_true", help="Disable preview rendering")
    
    args = parser.parse_args()
    
    try:
        scale_tuple = tuple(map(float, args.scale.split(",")))
    except ValueError:
        print("Error: --scale must be three comma-separated numbers (e.g., 1.0,2.0,0.1)")
        sys.exit(1)
        
    print(f"--- MStorm Asset Forge: START for '{args.name}' ---")
    
    # 1. Prepare Package Directory
    try:
        package_path = prepare_package_dir(args.output_dir, args.name)
        print(f"Forge: Created package directory: {package_path}")
    except Exception as e:
        print(f"Forge: CRITICAL ERROR - Package directory creation failed: {e}")
        sys.exit(1)
        
    # Standard internal asset names
    asset_file = "asset.obj"
    asset_path = os.path.join(package_path, asset_file)
    
    preview_file = "preview.png"
    preview_path = os.path.join(package_path, preview_file) if not args.no_preview else None
    
    # 2. Generate and Execute BPY script
    bpy_script = generate_bpy_script(
        args.name, args.primitive, scale_tuple, 
        output_path=asset_path, 
        preview_path=preview_path
    )
    
    print(f"Forge: Executing Blender headless (OBJ/MTL" + (" + Preview" if preview_path else "") + ")...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 3. Handle Result and Finalize Manifest
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
            package_path, args.name, args.primitive, scale_tuple, 
            preview_file=final_preview
        )
        print(f"Forge: Manifest written to {manifest_path}")
        
        print(f"Forge: Successfully packaged '{args.name}' in {package_path}")
        print(f"--- MStorm Asset Forge: DONE ---")
    else:
        print(f"Forge: Blender execution FAILED.")
        print(f"Error Message: {result.get('message')}")
        # Non-fatal preview check: If OBJ exists, we might still want to package it? 
        # For MVP Slice 2, we stick to the plan: if result is success, we are good.
        # If Blender failed entirely, we exit.
        sys.exit(1)

if __name__ == "__main__":
    main()
