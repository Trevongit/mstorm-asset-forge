import argparse
import os
import sys
import json
import re
import datetime
import uuid
from forge.generator import generate_bpy_script
from forge.packager import (
    prepare_package_dir, write_manifest, write_run_report, 
    update_global_registry, create_zip_archive, prune_stale_assets,
    sync_assets_to_project, get_library_list, get_asset_info
)
from forge.agent import interpret_prompt
from forge.safety import validate_snippet
from forge.validator import validate_asset
from blender.headless import execute_headless_blender

def forge_item(asset_params, options, global_command, dry_run=False, llm_metadata=None):
    """
    Processes a single asset request.
    Returns (bool success, str message, dict result_info)
    """
    name = asset_params.get("name", "prop")
    # Resolve preset if specified
    preset_name = options.get("preset")
    primitive = asset_params.get("primitive", "cube")
    
    scale_tuple = tuple(map(float, asset_params.get("scale", [1.0, 1.0, 1.0])))
    
    shading = options.get("shading", "flat")
    bevel = float(options.get("bevel", 0.0))
    subdivisions = int(options.get("subdivisions", 0))
    auto_smooth = bool(options.get("auto_smooth", False))
    fmt = options.get("format", "obj")
    category = options.get("category")
    
    # Material parameters
    base_color = options.get("base_color", (0.8, 0.8, 0.8))
    metallic = float(options.get("metallic", 0.0))
    roughness = float(options.get("roughness", 0.5))
    emission_color = options.get("emission_color", (0.0, 0.0, 0.0))
    emission_strength = float(options.get("emission_strength", 0.0))
    alpha = float(options.get("alpha", 1.0))
    mat_name = options.get("material_name", "ForgeMaterial")
    
    python_code = options.get("python_code")
    experimental_mode = options.get("experimental_mode", False)
    
    author = options.get("author", "MStorm Forge")
    output_dir = options.get("output_dir", "outputs")
    no_preview = options.get("no_preview", False)
    tags_list = options.get("tags", [])
    do_zip = options.get("zip", False)

    result_info = {
        "name": name,
        "primitive": primitive if not preset_name else f"preset:{preset_name}",
        "status": "failed",
        "package_path": None,
        "preview_path": None,
        "archive_path": None,
        "validation": None,
        "error": None
    }

    # Validation
    if bevel < 0: 
        result_info["error"] = "Bevel must be non-negative"
        return False, result_info["error"], result_info
    if not (0 <= subdivisions <= 5): 
        result_info["error"] = "Subdivisions must be between 0 and 5"
        return False, result_info["error"], result_info
    if not (0.0 <= metallic <= 1.0):
        result_info["error"] = "Metallic must be between 0.0 and 1.0"
        return False, result_info["error"], result_info
    if not (0.0 <= roughness <= 1.0):
        result_info["error"] = "Roughness must be between 0.0 and 1.0"
        return False, result_info["error"], result_info
    if not (0.0 <= alpha <= 1.0):
        result_info["error"] = "Alpha must be between 0.0 and 1.0"
        return False, result_info["error"], result_info
    if emission_strength < 0:
        result_info["error"] = "Emission strength must be non-negative"
        return False, result_info["error"], result_info

    # Sandbox Snippet Validation
    if python_code:
        is_valid, err = validate_snippet(python_code)
        if not is_valid:
            result_info["error"] = f"Sandbox Validation Failed: {err}"
            return False, result_info["error"], result_info

    print(f"\n>>> Forge Item: '{name}' ({primitive if not preset_name else f'PRESET:{preset_name}'}) <<<")
    
    if dry_run:
        print(f"DRY RUN: Validation passed for '{name}'.")
        if python_code:
            print(f"DRY RUN: Python Snippet:\n---\n{python_code}\n---")
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
        base_color=base_color, metallic=metallic, roughness=roughness,
        emission_color=emission_color, emission_strength=emission_strength,
        alpha=alpha, material_name=mat_name,
        output_path=asset_path, 
        preview_path=preview_path,
        export_format=fmt,
        python_code=python_code,
        preset_name=preset_name
    )
    
    print(f"Forge: Executing Blender headless ({primitive if not preset_name else preset_name})...")
    result = execute_headless_blender(bpy_script, timeout=60)
    
    # 3. Handle Result
    if result.get("status") == "success":
        print(f"Forge: Blender execution SUCCESS.")
        
        # --- Artifact Integrity Gate ---
        if not os.path.exists(asset_path):
            result_info["status"] = "failed"
            result_info["error"] = f"Integrity Failure: Entry point file {asset_file} was not created."
            print(f"Forge: {result_info['error']}")
            return False, result_info["error"], result_info
            
        if os.path.getsize(asset_path) == 0:
            result_info["status"] = "failed"
            result_info["error"] = f"Integrity Failure: Entry point file {asset_file} is empty (0 bytes)."
            print(f"Forge: {result_info['error']}")
            return False, result_info["error"], result_info
            
        print(f"Forge: Artifact integrity verified ({asset_file}).")

        # Stats Extraction
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
            
        # Optional ZIP creation
        archive_file = None
        if do_zip:
            print(f"Forge: Creating ZIP archive...")
            archive_file = create_zip_archive(package_path)
            if archive_file:
                result_info["archive_path"] = archive_file
                print(f"Forge: ZIP created: {archive_file}")

        # --- Phase 4: Asset Validation ---
        val_success, val_errors, val_warnings, val_meta = validate_asset(
            package_path, asset_params, options, geometry_stats=geometry_stats
        )
        
        validation_report = {
            "success": val_success,
            "errors": val_errors,
            "warnings": val_warnings,
            "metadata": val_meta
        }
        result_info["validation"] = validation_report

        if not val_success:
            print(f"Forge: Asset Validation FAILED: {', '.join(val_errors)}")
            result_info["status"] = "failed"
            result_info["error"] = f"Validation Errors: {', '.join(val_errors)}"
            return False, result_info["error"], result_info

        if val_warnings:
            print(f"Forge: Validation Warnings: {', '.join(val_warnings)}")

        # Write manifest last to reflect actual content
        archive_name_placeholder = f"{os.path.basename(package_path)}.zip" if do_zip else None

        # Capture the asset_id and timestamp returned by write_manifest
        manifest_path, asset_id, timestamp = write_manifest(
            package_path, name, primitive, scale_tuple, 
            tags=tags_list,
            preview_file=final_preview,
            author=author,
            creation_command=global_command,
            geometry_stats=geometry_stats,
            parametric_options={
                "bevel": bevel, "subdivisions": subdivisions, 
                "auto_smooth": auto_smooth, "shading": shading,
                "base_color": base_color, "metallic": metallic, "roughness": roughness,
                "emission_color": emission_color, "emission_strength": emission_strength,
                "alpha": alpha, "material_name": mat_name
            },
            source_type="agent_bpy_sandbox" if python_code else "primitive",
            experimental_mode=experimental_mode,
            llm_metadata=llm_metadata,
            entry_point=asset_file,
            format=fmt,
            archive_file=archive_name_placeholder,
            validation_results=validation_report,
            preset_name=preset_name
        )
        print(f"Forge: Manifest written to {package_path}/manifest.json")
        
        # --- Update Global Registry ---
        registry_info = {
            "asset_id": asset_id,
            "name": name,
            "category": category,
            "format": fmt,
            "entry_point": os.path.join(rel_package_path, asset_file),
            "preview_path": result_info["preview_path"],
            "archive_path": archive_file,
            "package_path": rel_package_path,
            "timestamp": timestamp,
            "validation_success": val_success
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
    parser = argparse.ArgumentParser(description="MStorm Asset Forge - Production Pipeline")
    parser.add_argument("-f", "--file", type=str, help="Path to a JSON request file")
    parser.add_argument("-p", "--prompt", type=str, help="Natural language request")
    parser.add_argument("--llm-batch", action="store_true", help="Use LLM to generate a batch of requests")
    parser.add_argument("--prompt-to-bpy", action="store_true", help="Experimental: Allow LLM to generate geometry code")
    parser.add_argument("--llm", action="store_true", help="Use LLM for prompt interpretation")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "gemini", "mock"], help="LLM provider")
    parser.add_argument("--model", type=str, help="LLM model name")
    parser.add_argument("--dry-run", action="store_true", help="Interpret and validate without running Blender")
    
    # Utilities
    parser.add_argument("--prune", action="store_true", help="Remove stale asset folders and archives not in registry")
    parser.add_argument("--sync", type=str, help="Path to an external project assets directory to sync registry items")
    parser.add_argument("--sync-name", type=str, help="Limit sync to a specific asset name")
    parser.add_argument("--sync-category", type=str, help="Limit sync to a specific category")
    
    # Explorer
    parser.add_argument("--list", action="store_true", help="List all assets in the registry")
    parser.add_argument("--info", type=str, help="Show detailed information for a specific asset name")
    parser.add_argument("--sort", type=str, choices=["name", "date"], default="date", help="Sort library list")
    parser.add_argument("--json", action="store_true", help="Output explorer results as JSON")
    parser.add_argument("--category", type=str, help="Filter list by category")
    parser.add_argument("--format", type=str, choices=["obj", "glb"], help="Filter list by format")
    
    # Deterministic Arguments
    parser.add_argument("--name", type=str, help="Asset name")
    parser.add_argument("--primitive", type=str, choices=["cube", "sphere", "cylinder", "plane", "table", "stool", "crate"], help="Primitive or Modular Prop type")
    parser.add_argument("--preset", type=str, help="Deterministic Preset/Archetype name")
    parser.add_argument("--scale", type=str, help="Comma-separated scale (x,y,z)")
    parser.add_argument("--shading", type=str, choices=["flat", "smooth"], help="Shading type")
    parser.add_argument("--bevel", type=float, help="Bevel width")
    parser.add_argument("--subdivisions", type=int, help="Subdivision levels (0-5)")
    parser.add_argument("--auto-smooth", action="store_true", default=None, help="Enable auto-smooth")
    # parser.add_argument("--format" is already defined in Explorer section above
    parser.add_argument("--zip", action="store_true", help="Create a ZIP archive of the package")
    
    # PBR Material Arguments
    parser.add_argument("--color", type=str, help="Base color (Hex string like #FFD700)")
    parser.add_argument("--metallic", type=float, help="Metallic value (0.0-1.0)")
    parser.add_argument("--roughness", type=float, help="Roughness value (0.0-1.0)")
    parser.add_argument("--emission-color", type=str, help="Emission color (Hex string)")
    parser.add_argument("--emission-strength", type=float, help="Emission strength (>= 0)")
    parser.add_argument("--alpha", type=float, help="Alpha transparency (0.0-1.0)")
    parser.add_argument("--material-name", type=str, help="Custom material name")
    
    parser.add_argument("--author", type=str, help="Asset author name")
    parser.add_argument("--output-dir", type=str, help="Output root directory")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--no-preview", action="store_true", default=None, help="Disable preview rendering")
    
    args = parser.parse_args()
    full_command = " ".join(sys.argv)
    output_dir_final = args.output_dir or "outputs"

    # --- Explorer Path ---
    if args.list:
        assets = get_library_list(
            output_dir_final, 
            category_filter=args.category, 
            format_filter=args.format,
            sort_by=args.sort
        )
        if args.json:
            print(json.dumps(assets, indent=2))
        else:
            print(f"Forge: Library Assets in '{output_dir_final}' (sorted by {args.sort}):")
            if not assets:
                print(" No assets found.")
            for a in assets:
                cat = f" [{a.get('category')}]" if a.get('category') else ""
                val_status = "OK" if a.get('validation_success') else "WARN"
                print(f" - {a.get('name')}{cat} ({a.get('format')}) [{val_status}] -> {a.get('package_path')}")
        sys.exit(0)

    if args.info:
        info = get_asset_info(output_dir_final, args.info)
        if not info:
            print(f"Forge: Asset '{args.info}' not found in registry.")
            sys.exit(1)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"\n--- Asset Info: {args.info} ---")
            print(json.dumps(info, indent=2))
        sys.exit(0)

    # --- Pruning Path ---
    if args.prune:
        print(f"Forge: Pruning stale assets in '{output_dir_final}'...")
        try:
            summary = prune_stale_assets(output_dir_final, dry_run=args.dry_run)
            if args.dry_run:
                print(f"\nPrune Dry Run Summary: Found {summary['found']} items to remove.")
            else:
                print(f"\nPrune Complete: Removed {summary['removed_folders']} folders and {summary['removed_zips']} zips.")
            print(f"Protected items skipped: {summary['protected_count']}")
            if summary['errors'] > 0:
                print(f"Errors encountered: {summary['errors']}")
            sys.exit(0)
        except Exception as e:
            print(f"Forge Error: {e}")
            sys.exit(1)

    if args.sync:
        print(f"Forge: Syncing registry assets to '{args.sync}'...")
        try:
            summary = sync_assets_to_project(
                output_dir_final, args.sync, 
                name_filter=args.sync_name, 
                category_filter=args.sync_category, 
                dry_run=args.dry_run
            )
            if args.dry_run:
                print(f"\nSync Dry Run Summary: Selected {summary['selected']} assets for sync.")
            else:
                print(f"\nSync Complete: Copied {summary['folders_copied']} folders and {summary['zips_copied']} zips.")
            if summary['warnings'] > 0:
                print(f"Warnings: {summary['warnings']}")
            if summary['errors'] > 0:
                print(f"Errors: {summary['errors']}")
            sys.exit(0)
        except Exception as e:
            print(f"Forge Error: {e}")
            sys.exit(1)

    requests = []
    global_llm_metadata = None

    # 1. Resolve Requests
    if args.prompt:
        if (args.prompt_to_bpy or args.llm_batch) and not args.llm:
            mode = "prompt-to-bpy" if args.prompt_to_bpy else "llm-batch"
            print(f"Error: --{mode} requires --llm.")
            sys.exit(1)
            
        print(f"Agent: Interpreting prompt: '{args.prompt}' (Sandbox: {args.prompt_to_bpy}, Batch: {args.llm_batch})...")
        result, msg = interpret_prompt(args.prompt, use_llm=args.llm, 
                                    provider=args.provider, model=args.model,
                                    sandbox_mode=args.prompt_to_bpy,
                                    batch_mode=args.llm_batch)
        if not result:
            print(f"Agent Error: {msg}")
            sys.exit(1)
        
        print(f"Agent: Success.")
        print(json.dumps(result, indent=2))
        
        if isinstance(result, list):
            requests = result
        else:
            requests = [result]

        for req in requests:
            if args.prompt_to_bpy:
                if "options" not in req: req["options"] = {}
                req["options"]["experimental_mode"] = True
            
        if args.llm:
            global_llm_metadata = {"provider": args.provider, "model": args.model or "default"}
            
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
        # PBR conversion for RGB lists in CLI? No, simple string for now.
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
                "preset": args.preset,
                "base_color": args.color or "#CCCCCC",
                "metallic": args.metallic or 0.0,
                "roughness": args.roughness or 0.5,
                "emission_color": args.emission_color or "#000000",
                "emission_strength": args.emission_strength or 0.0,
                "alpha": args.alpha or 1.0,
                "material_name": args.material_name or "ForgeMaterial",
                "author": args.author or "MStorm Forge",
                "output_dir": output_dir_final,
                "tags": [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else [],
                "no_preview": args.no_preview if args.no_preview is not None else False
            }
        }]

    # 2. Process Requests
    total = len(requests)
    is_batch = total > 1
    asset_results = []

    if args.dry_run:
        print("--- DRY RUN MODE ENABLED ---")

    print(f"--- MStorm Asset Forge: Processing {total} request(s) ---")

    for i, req in enumerate(requests):
        asset_data = req.get("asset", {})
        options_data = req.get("options", {})

        if args.file or args.prompt:
            missing = []
            if "name" not in asset_data: missing.append("asset.name")
            if not options_data.get("experimental_mode") and not options_data.get("preset") and "primitive" not in asset_data: 
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
            if args.preset is not None: options_data["preset"] = args.preset
            if args.color is not None: options_data["base_color"] = args.color
            if args.metallic is not None: options_data["metallic"] = args.metallic
            if args.roughness is not None: options_data["roughness"] = args.roughness
            if args.emission_color is not None: options_data["emission_color"] = args.emission_color
            if args.emission_strength is not None: options_data["emission_strength"] = args.emission_strength
            if args.alpha is not None: options_data["alpha"] = args.alpha
            if args.material_name is not None: options_data["material_name"] = args.material_name
            if args.tags is not None: 
                options_data["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]

        success, msg, result_info = forge_item(asset_data, options_data, full_command, dry_run=args.dry_run, llm_metadata=global_llm_metadata)
        result_info["index"] = i
        asset_results.append(result_info)

    # 3. Final Summary & Report
    success_count = sum(1 for r in asset_results if r["status"] in ["success", "dry_run"])
    fail_count = total - success_count

    run_metadata = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
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
