import json
import os
import datetime
import uuid

def prepare_package_dir(output_root, asset_name):
    """
    Creates a standardized package directory.
    """
    timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"{timestamp_folder}_{asset_name}"
    package_path = os.path.join(output_root, package_name)
    os.makedirs(package_path, exist_ok=True)
    return package_path

def write_manifest(package_path, asset_name, primitive, scale, 
                   tags=None, preview_file=None, author="MStorm Forge", 
                   creation_command=None, geometry_stats=None, 
                   parametric_options=None, source_type="primitive",
                   experimental_mode=False, llm_metadata=None, 
                   entry_point=None, format="obj", version="1.0.0"):
    """
    Writes a manifest.json file to the package directory.
    """
    manifest_timestamp = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    asset_id = str(uuid.uuid4())
    
    final_tags = ["generated", "mvp", "prop", primitive.lower()]
    if experimental_mode:
        final_tags.append("experimental")

    if tags:
        for t in tags:
            t_clean = t.strip().lower()
            if t_clean and t_clean not in final_tags:
                final_tags.append(t_clean)
    
    provenance = {
        "source_type": source_type,
        "creation_command": creation_command or "Manual",
        "experimental_mode": experimental_mode
    }
    if llm_metadata:
        provenance.update(llm_metadata)

    manifest = {
        "asset_id": asset_id,
        "name": asset_name,
        "type": "static_prop",
        "format": format,
        "entry_point": entry_point,
        "version": version,
        "author": author,
        "generator": "MStorm Asset Forge v0.1",
        "timestamp": manifest_timestamp,
        "provenance": provenance,
        "metadata": {
            "primitive": primitive,
            "scale": scale,
            "unit_system": "metric",
            "unit_scale": "1.0 unit = 1.0 meter",
            "is_rigged": False
        },
        "tags": final_tags
    }
    
    if parametric_options:
        manifest["metadata"]["parametric_options"] = parametric_options
    
    if preview_file:
        manifest["preview_image"] = preview_file
    if geometry_stats:
        manifest["geometry_stats"] = geometry_stats
        
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return manifest_path, asset_id, manifest_timestamp

def write_run_report(output_dir, run_metadata, asset_results):
    """
    Writes a summary run_report.json to the output directory.
    """
    report = {
        "run_metadata": run_metadata,
        "assets": asset_results
    }
    
    report_path = os.path.join(output_dir, "run_report.json")
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        return report_path
    except Exception as e:
        print(f"Forge: WARNING - Could not write run report to {report_path}: {e}")
        return None

def update_global_registry(output_root, asset_info):
    """
    Upserts an asset entry into the global registry.json using a logical key.
    The registry represents the LATEST version of each unique asset identity.
    """
    registry_path = os.path.join(output_root, "registry.json")
    
    registry = {"last_updated": None, "assets": []}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except Exception as e:
            print(f"Forge: WARNING - Could not read registry, starting fresh: {e}")

    # LOGICAL KEY: name + category + format
    # This ensures the registry only keeps the latest version of a specific logical asset.
    def get_logical_key(a):
        # Normalize category to handle None/missing consistently
        cat = a.get('category')
        if cat is None: cat = ""
        return f"{a.get('name')}|{cat}|{a.get('format')}"

    new_key = get_logical_key(asset_info)
    assets = registry.get("assets", [])
    
    updated_assets = []
    found = False
    for a in assets:
        if get_logical_key(a) == new_key:
            updated_assets.append(asset_info)
            found = True
        else:
            updated_assets.append(a)
            
    if not found:
        updated_assets.append(asset_info)
        
    registry["assets"] = updated_assets
    registry["last_updated"] = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    
    try:
        os.makedirs(output_root, exist_ok=True)
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=4)
        return registry_path
    except Exception as e:
        print(f"Forge: WARNING - Could not update global registry: {e}")
        return None
