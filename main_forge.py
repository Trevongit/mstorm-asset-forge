import argparse
import os
import sys
import json
from forge.generator import generate_bpy_script
from forge.packager import prepare_package_dir, write_manifest
from blender.headless import execute_headless_blender

def forge_item(asset_params, options, global_command):
    """
    Processes a single asset request.
    Returns (bool success, str message)
    """
    name = asset_params.get("name", "prop")
    primitive = asset_params.get("primitive", "cube")
    scale_tuple = tuple(map(float, asset_params.get("scale", [1.0, 1.0, 1.0])))
    
    shading = options.get("shading", "flat")
    author = options.get("author", "MStorm Forge")
    output_dir = options.get("output_dir", "outputs")
    no_preview = options.get("no_preview", False)
    tags_list = options.get("tags", [])

    print(f"\n>>> Forge Item: '{name}' ({primitive}) <<<")
    
    # 1. Prepare Package Directory
    try:
        package_path = prepare_package_dir(output_dir, name)
        print(f"Forge: Created package directory: {package_path}")
    except Exception as e:
        return False, f"Package directory creation failed: {e}"
        
    # Standard names
    asset_file = "asset.obj"
    asset_path = os.path.join(package_path, asset_file)
    preview_file = "preview.png"
    preview_path = os.path.join(package_path, preview_file) if not no_preview else None
    
    # 2. Generate and Execute BPY script
    bpy_script = generate_bpy_script(
        name, primitive, scale_tuple, shading=shading,
        output_path=asset_path, 
        preview_path=preview_path
    )
    
    print(f"Forge: Executing Blender headless ({primitive} @ {shading} shading)...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 3. Handle Result and Finalize Manifest
    if result.get("status") == "success":
        final_preview = None
        if preview_path and os.path.exists(preview_path):
            final_preview = preview_file
            print(f"Forge: Preview rendered successfully.")
            
        manifest_path = write_manifest(
            package_path, name, primitive, scale_tuple, 
            tags=tags_list,
            preview_file=final_preview,
            author=author,
            creation_command=global_command
        )
        print(f"Forge: Manifest written to {manifest_path}")
        print(f"Forge: Successfully packaged '{name}'")
        return True, "Success"
    else:
        err_msg = result.get('message', 'Unknown Blender error')
        print(f"Forge: Blender execution FAILED: {err_msg}")
        return False, err_msg

def main():
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - OBJ Baseline Pipeline")
    parser.add_argument("-f", "--file", type=str, help="Path to a JSON request file")
    parser.add_argument("--name", type=str, help="Asset name")
    parser.add_argument("--primitive", type=str, choices=["cube", "sphere", "cylinder", "plane"], help="Primitive type")
    parser.add_argument("--scale", type=str, help="Comma-separated scale (x,y,z)")
    parser.add_argument("--shading", type=str, choices=["flat", "smooth"], help="Shading type")
    parser.add_argument("--author", type=str, help="Asset author name")
    parser.add_argument("--output-dir", type=str, help="Output root directory")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--no-preview", action="store_true", default=None, help="Disable preview rendering")
    
    args = parser.parse_args()
    full_command = " ".join(sys.argv)
    
    requests = []

    # 1. Resolve Requests
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: Request file not found: {args.file}")
            sys.exit(1)
        
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                # Batch Mode
                requests = data
            elif isinstance(data, dict):
                # Single Request Mode (legacy/standard)
                requests = [data]
            else:
                print("Error: Invalid JSON root. Must be an object or a list.")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse request file JSON: {e}")
            sys.exit(1)
    else:
        # Pure CLI Mode: Create a synthetic request
        requests = [{
            "asset": {
                "name": args.name or "prop",
                "primitive": args.primitive or "cube",
                "scale": list(map(float, args.scale.split(","))) if args.scale else [1.0, 1.0, 1.0]
            },
            "options": {
                "shading": args.shading or "flat",
                "author": args.author or "MStorm Forge",
                "output_dir": args.output_dir or "outputs",
                "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
                "no_preview": args.no_preview if args.no_preview is not None else False
            }
        }]

    # 2. Process Requests
    total = len(requests)
    is_batch = total > 1
    results = []

    print(f"--- MStorm Asset Forge: Processing {total} request(s) ---")

    for i, req in enumerate(requests):
        asset_data = req.get("asset", {})
        options_data = req.get("options", {})

        # Validation for JSON-sourced items
        if args.file:
            missing = []
            if "name" not in asset_data: missing.append("asset.name")
            if "primitive" not in asset_data: missing.append("asset.primitive")
            if missing:
                print(f"\n[Item {i}] Error: Missing required fields: {', '.join(missing)}")
                results.append((False, asset_data.get("name", f"item_{i}"), "Missing fields"))
                continue

        # Global CLI Overrides (Applied to every item)
        if args.output_dir is not None: options_data["output_dir"] = args.output_dir
        if args.no_preview is not None: options_data["no_preview"] = args.no_preview
        if args.author is not None: options_data["author"] = args.author
        
        # Single-item explicit overrides (only relevant if not in batch mode or applied to all)
        # For Slice 8, as per rules: name/primitive/scale only override in SINGLE mode
        if not is_batch:
            if args.name is not None: asset_data["name"] = args.name
            if args.primitive is not None: asset_data["primitive"] = args.primitive
            if args.scale is not None: asset_data["scale"] = list(map(float, args.scale.split(",")))
            if args.shading is not None: options_data["shading"] = args.shading
            if args.tags is not None: 
                options_data["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]

        success, msg = forge_item(asset_data, options_data, full_command)
        results.append((success, asset_data.get("name"), msg))

    # 3. Final Summary
    success_count = sum(1 for r in results if r[0])
    fail_count = total - success_count

    print(f"\n--- MStorm Asset Forge: {'BATCH ' if is_batch else ''}COMPLETE ---")
    print(f"Total:   {total}")
    print(f"Success: {success_count}")
    print(f"Failed:  {fail_count}")
    
    if fail_count > 0:
        print("\nFailures:")
        for i, (success, name, msg) in enumerate(results):
            if not success:
                print(f" - [Index {i}] {name}: {msg}")
        sys.exit(1)

if __name__ == "__main__":
    main()
