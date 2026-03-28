import argparse
import os
import sys
from forge.generator import generate_bpy_script
from forge.packager import create_asset_package
from blender.headless import execute_headless_blender

def main():
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - OBJ Baseline Pipeline")
    parser.add_argument("--name", type=str, default="prop", help="Asset name")
    parser.add_argument("--primitive", type=str, default="cube", choices=["cube", "sphere", "cylinder", "plane"], help="Primitive type")
    parser.add_argument("--scale", type=str, default="1.0,1.0,1.0", help="Comma-separated scale (x,y,z)")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output root directory")
    parser.add_argument("--tags", type=str, default="", help="Comma-separated tags")
    
    args = parser.parse_args()
    
    try:
        scale_tuple = tuple(map(float, args.scale.split(",")))
    except ValueError:
        print("Error: --scale must be three comma-separated numbers (e.g., 1.0,2.0,0.1)")
        sys.exit(1)
        
    print(f"--- MStorm Asset Forge: START for '{args.name}' ---")
    
    # 1. Prepare Package Structure
    try:
        package_path, manifest_path = create_asset_package(
            args.output_dir, args.name, args.primitive, scale_tuple
        )
        print(f"Forge: Created package directory: {package_path}")
    except Exception as e:
        print(f"Forge: CRITICAL ERROR - Package creation failed: {e}")
        sys.exit(1)
        
    # Standard internal asset name
    asset_file = "asset.obj"
    asset_path = os.path.join(package_path, asset_file)
    
    # 2. Generate and Execute BPY script
    bpy_script = generate_bpy_script(
        args.name, args.primitive, scale_tuple, output_path=asset_path
    )
    
    print(f"Forge: Executing Blender headless (OBJ/MTL)...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 3. Handle Result
    if result.get("status") == "success":
        print(f"Forge: Blender export SUCCESS.")
        print(f"Forge: Successfully packaged '{args.name}' in {package_path}")
        print(f"--- MStorm Asset Forge: DONE ---")
    else:
        print(f"Forge: Blender export FAILED.")
        print(f"Error Message: {result.get('message')}")
        # Append error output if available
        if isinstance(result.get("result"), dict) and result.get("result").get("result"):
             print(f"Blender Output:\n{result.get('result').get('result')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
