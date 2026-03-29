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
                   creation_command=None, geometry_stats=None, version="1.0.0"):
    """
    Writes a manifest.json file to the package directory.
    """
    manifest_timestamp = datetime.datetime.now(datetime.UTC).isoformat() + "Z"
    asset_id = str(uuid.uuid4())
    
    final_tags = ["generated", "mvp", "prop", primitive.lower()]
    if tags:
        for t in tags:
            t_clean = t.strip().lower()
            if t_clean and t_clean not in final_tags:
                final_tags.append(t_clean)
    
    manifest = {
        "asset_id": asset_id,
        "name": asset_name,
        "type": "static_prop",
        "format": "obj",
        "version": version,
        "author": author,
        "generator": "MStorm Asset Forge v0.1",
        "timestamp": manifest_timestamp,
        "provenance": {
            "source_type": "primitive",
            "creation_command": creation_command or "Manual"
        },
        "metadata": {
            "primitive": primitive,
            "scale": scale,
            "unit_system": "metric",
            "unit_scale": "1.0 unit = 1.0 meter",
            "is_rigged": False
        },
        "tags": final_tags
    }
    
    if preview_file:
        manifest["preview_image"] = preview_file
    if geometry_stats:
        manifest["geometry_stats"] = geometry_stats
        
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return manifest_path

def write_run_report(output_dir, run_metadata, asset_results):
    """
    Writes a summary run_report.json to the output directory.
    Non-fatal if writing fails.
    """
    report = {
        "run_metadata": run_metadata,
        "assets": asset_results
    }
    
    report_path = os.path.join(output_dir, "run_report.json")
    try:
        # Ensure output dir exists (it should, but just in case)
        os.makedirs(output_dir, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        return report_path
    except Exception as e:
        print(f"Forge: WARNING - Could not write run report to {report_path}: {e}")
        return None
