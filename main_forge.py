import argparse
import os
import sys
import json
import re
import datetime
from forge.generator import generate_bpy_script
from forge.packager import prepare_package_dir, write_manifest, write_run_report, update_global_registry, create_zip_archive
from forge.agent import interpret_prompt
from forge.safety import validate_snippet
from blender.headless import execute_headless_blender

def forge_item(asset_params, options, global_command, dry_run=False, llm_metadata=None):
    """
    Processes a single asset request.
    Returns (bool success, str message, dict result_info)
    """
    name = asset_params.get("name", "prop")
    primitive = asset_params.get("primitive", "cube")
    scale_tuple = tuple(map(float, asset_params.get("scale", [1.0, 1.0, 1.0])))
    
    shading = options.get("shading", "flat")
    bevel = float(options.get("bevel", 0.0))
    subdivisions = int(options.get("subdivisions", 0))
    auto_smooth = bool(options.get("auto_smooth", False))
    fmt = options.get("format", "obj")
    category = options.get("category")
    
    python_code = options.get("python_code")
    experimental_mode = options.get("experimental_mode", False)
    
    author = options.get("author", "MStorm Forge")
    output_dir = options.get("output_dir", "outputs")
    no_preview = options.get("no_preview", False)
    tags_list = options.get("tags", [])
    do_zip = options.get("zip", False)

    result_info = {
        "name": name,
        "primitive": primitive,
        "status": "failed",
        "package_path": None,
        "preview_path": None,
        "archive_path": None,
        "error": None
    }

    # Validation
    if bevel < 0: 
        result_info["error"] = "Bevel must be non-negative"
        return False, result_info["error"], result_info
    if not (0 <= subdivisions <= 5): 
        result_info["error"] = "Subdivisions must be between 0 and 5"
        return False, result_info["error"], result_info

    # Sandbox Snippet Validation
    if python_code:
        is_valid, err = validate_snippet(python_code)
        if not is_valid:
            result_info["error"] = f"Sandbox Validation Failed: {err}"
            return False, result_info["error"], result_info

    print(f"\n>>> Forge Item: '{name}' ({primitive}) <<<")
    
    if dry_run:
        print(f"DRY RUN: Validation passed for '{name}'.")
        result_info["status"] = "dry_run"
        return True, "Dry run successful", result_info

    # 1. Prepare Package Directory
    try:
        package_path = prepare_package_dir(output_dir, name)
        rel_package_path = os.path.relpath(package_path, output_dir)
        result_info["package_path"] = rel_package_path
        print(f"Forge: Created package directory: {package_path}")
    except Exception as e:
        result_info["error"] = str(e)
        return False, f"Package directory creation failed: {e}", result_info
        
    asset_file = f"asset.{fmt}"
    asset_path = os.path.join(package_path, asset_file)
    preview_file = "preview.png"
    preview_path = os.path.join(package_path, preview_file) if not no_preview else None
    
    # 2. Generate and Execute BPY script
    bpy_script = generate_bpy_script(
        name, primitive, scale_tuple, shading=shading,
        bevel=bevel, subdivisions=subdivisions, auto_smooth=auto_smooth,
        output_path=asset_path, 
        preview_path=preview_path,
        export_format=fmt,
        python_code=python_code
    )
    
    print(f"Forge: Executing Blender headless ({primitive})...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 3. Handle Result
    if result.get("status") == "success":
        print(f"Forge: Blender execution SUCCESS.")
        
        geometry_stats = None
        blender_stdout = result.get("result", {}).get("result", "")
        match = re.search(r"FORGE_STATS: ({.*})", blender_stdout)
        if match:
            try:
                geometry_stats = json.loads(match.group(1))
                print(f"Forge: Extracted stats - Vertices: {geometry_stats.get('vertex_count')}, Faces: {geometry_stats.get('face_count')}")
            except Exception: pass

        final_preview = None
        if preview_path and os.path.exists(preview_path):
            final_preview = preview_file
            result_info["preview_path"] = os.path.join(rel_package_path, preview_file)
            print(f"Forge: Preview rendered successfully.")
            
        parametric_options = {
            "bevel": bevel,
            "subdivisions": subdivisions,
            "auto_smooth": auto_smooth,
            "shading": shading
        }

        source_type = "agent_bpy_sandbox" if python_code else "primitive"

        # --- Phase 1: Write Manifest (with archive placeholder if needed) ---
        # Note: We use the archive name even before creation so it's in the manifest
        # which will be zipped!
        archive_name_placeholder = f"{os.path.basename(package_path)}.zip" if do_zip else None

        manifest_path, asset_id, timestamp = write_manifest(
            package_path, name, primitive, scale_tuple, 
            tags=tags_list,
            preview_file=final_preview,
            author=author,
            creation_command=global_command,
            geometry_stats=geometry_stats,
            parametric_options=parametric_options,
            source_type=source_type,
            experimental_mode=experimental_mode,
            llm_metadata=llm_metadata,
            entry_point=asset_file,
            format=fmt,
            archive_file=archive_name_placeholder
        )
        print(f"Forge: Manifest written to {manifest_path}")
        
        # --- Phase 2: Create ZIP (Includes the manifest just written) ---
        archive_file = None
        if do_zip:
            print(f"Forge: Creating ZIP archive...")
            archive_file = create_zip_archive(package_path)
            if archive_file:
                result_info["archive_path"] = archive_file
                print(f"Forge: ZIP created: {archive_file}")

        # --- Phase 3: Update Global Registry ---
        registry_info = {
            "asset_id": asset_id,
            "name": name,
            "category": category,
            "format": fmt,
            "entry_point": os.path.join(rel_package_path, asset_file),
            "preview_path": result_info["preview_path"],
            "archive_path": archive_file,
            "package_path": rel_package_path,
            "timestamp": timestamp
        }
        update_global_registry(output_dir, registry_info)
        
        print(f"Forge: Successfully packaged and indexed '{name}'")
        result_info["status"] = "success"
        return True, "Success", result_info
    else:
        err_msg = result.get('message', 'Unknown Blender error')
        print(f"Forge: Blender execution FAILED: {err_msg}")
        result_info["error"] = err_msg
        return False, err_msg, result_info

def main():
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - OBJ/GLB Production Pipeline")
    parser.add_argument("-f", "--file", type=str, help="Path to a JSON request file")
    parser.add_argument("-p", "--prompt", type=str, help="Natural language request")
    parser.add_argument("--prompt-to-bpy", action="store_true", help="Experimental: Allow LLM to generate geometry code")
    parser.add_argument("--llm", action="store_true", help="Use LLM for prompt interpretation")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "gemini", "mock"], help="LLM provider")
    parser.add_argument("--model", type=str, help="LLM model name")
    parser.add_argument("--dry-run", action="store_true", help="Interpret and validate without running Blender")
    
    parser.add_argument("--name", type=str, help="Asset name")
    parser.add_argument("--primitive", type=str, choices=["cube", "sphere", "cylinder", "plane"], help="Primitive type")
    parser.add_argument("--scale", type=str, help="Comma-separated scale (x,y,z)")
    parser.add_argument("--shading", type=str, choices=["flat", "smooth"], help="Shading type")
    parser.add_argument("--bevel", type=float, help="Bevel width")
    parser.add_argument("--subdivisions", type=int, help="Subdivision levels (0-5)")
    parser.add_argument("--auto-smooth", action="store_true", default=None, help="Enable auto-smooth")
    parser.add_argument("--format", type=str, choices=["obj", "glb"], help="Export format")
    parser.add_argument("--category", type=str, help="Asset category (e.g., furniture, decor)")
    parser.add_argument("--zip", action="store_true", help="Create a ZIP archive of the package")
    
    parser.add_argument("--author", type=str, help="Asset author name")
    parser.add_argument("--output-dir", type=str, help="Output root directory")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--no-preview", action="store_true", default=None, help="Disable preview rendering")
    
    args = parser.parse_args()
    full_command = " ".join(sys.argv)
    
    requests = []
    global_llm_metadata = None

    # 1. Resolve Requests
    if args.prompt:
        if args.prompt_to_bpy and not args.llm:
            print("Error: --prompt-to-bpy requires --llm.")
            sys.exit(1)
            
        print(f"Agent: Interpreting prompt: '{args.prompt}' (Sandbox: {args.prompt_to_bpy})...")
        req, msg = interpret_prompt(args.prompt, use_llm=args.llm, 
                                    provider=args.provider, model=args.model,
                                    sandbox_mode=args.prompt_to_bpy)
        if not req:
            print(f"Agent Error: {msg}")
            sys.exit(1)
        
        print(f"Agent: Success.")
        print(json.dumps(req, indent=2))
        
        if args.prompt_to_bpy:
            if "options" not in req: req["options"] = {}
            req["options"]["experimental_mode"] = True
            
        if args.llm:
            global_llm_metadata = {"provider": args.provider, "model": args.model or "default"}
            
        requests = [req]
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: Request file not found: {args.file}")
            sys.exit(1)
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
            requests = data if isinstance(data, list) else [data]
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse request file JSON: {e}")
            sys.exit(1)
    else:
        requests = [{
            "asset": {
                "name": args.name or "prop",
                "primitive": args.primitive or "cube",
                "scale": list(map(float, args.scale.split(","))) if args.scale else [1.0, 1.0, 1.0]
            },
            "options": {
                "shading": args.shading or "flat",
                "bevel": args.bevel or 0.0,
                "subdivisions": args.subdivisions or 0,
                "auto_smooth": args.auto_smooth if args.auto_smooth is not None else False,
                "format": args.format or "obj",
                "category": args.category,
                "zip": args.zip,
                "author": args.author or "MStorm Forge",
                "output_dir": args.output_dir or "outputs",
                "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
                "no_preview": args.no_preview if args.no_preview is not None else False
            }
        }]

    # 2. Process Requests
    total = len(requests)
    is_batch = total > 1
    asset_results = []
    output_dir_final = "outputs"

    if args.dry_run:
        print("--- DRY RUN MODE ENABLED ---")

    print(f"--- MStorm Asset Forge: Processing {total} request(s) ---")

    for i, req in enumerate(requests):
        asset_data = req.get("asset", {})
        options_data = req.get("options", {})

        if args.file or args.prompt:
            missing = []
            if "name" not in asset_data: missing.append("asset.name")
            if not options_data.get("experimental_mode") and "primitive" not in asset_data: 
                missing.append("asset.primitive")
            if missing:
                print(f"\n[Item {i}] Error: Missing required fields: {', '.join(missing)}")
                asset_results.append({
                    "index": i, "name": asset_data.get("name", f"item_{i}"), 
                    "status": "failed", "error": "Missing required fields"
                })
                continue

        if args.output_dir is not None: options_data["output_dir"] = args.output_dir
        if args.no_preview is not None: options_data["no_preview"] = args.no_preview
        if args.author is not None: options_data["author"] = args.author
        if args.category is not None: options_data["category"] = args.category
        if args.zip is True: options_data["zip"] = True
        
        output_dir_final = options_data.get("output_dir", "outputs")

        if not is_batch:
            if args.name is not None: asset_data["name"] = args.name
            if args.primitive is not None: asset_data["primitive"] = args.primitive
            if args.scale is not None: asset_data["scale"] = list(map(float, args.scale.split(",")))
            if args.shading is not None: options_data["shading"] = args.shading
            if args.bevel is not None: options_data["bevel"] = args.bevel
            if args.subdivisions is not None: options_data["subdivisions"] = args.subdivisions
            if args.auto_smooth is not None: options_data["auto_smooth"] = args.auto_smooth
            if args.format is not None: options_data["format"] = args.format
            if args.category is not None: options_data["category"] = args.category
            if args.zip is not None: options_data["zip"] = args.zip
            if args.tags is not None: 
                options_data["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]

        success, msg, result_info = forge_item(asset_data, options_data, full_command, dry_run=args.dry_run, llm_metadata=global_llm_metadata)
        result_info["index"] = i
        asset_results.append(result_info)

    # 3. Final Summary & Report
    success_count = sum(1 for r in asset_results if r["status"] in ["success", "dry_run"])
    fail_count = total - success_count

    run_metadata = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
        "command": full_command,
        "output_dir": output_dir_final,
        "total_count": total,
        "success_count": success_count,
        "fail_count": fail_count
    }

    print(f"\n--- MStorm Asset Forge: {'BATCH ' if is_batch else ''}COMPLETE ---")
    print(f"Total:   {total}")
    print(f"Success: {success_count}")
    print(f"Failed:  {fail_count}")
    
    if not args.dry_run:
        report_path = write_run_report(output_dir_final, run_metadata, asset_results)
        if report_path:
            print(f"Forge: Run report written to {report_path}")

    if fail_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
