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

def write_manifest(package_path, asset_name, primitive, scale, tags=None, preview_file=None, version="1.0.0"):
    """
    Writes a manifest.json file to the package directory.
    """
    manifest_timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    asset_id = str(uuid.uuid4())
    
    # 1. Build base tags
    final_tags = ["generated", "mvp", "prop", primitive.lower()]
    
    # 2. Add user-provided tags with deduplication
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
        "generator": "MStorm Asset Forge v0.1",
        "timestamp": manifest_timestamp,
        "metadata": {
            "primitive": primitive,
            "scale": scale,
            "unit_system": "metric",
            "is_rigged": False
        },
        "tags": final_tags
    }
    
    if preview_file:
        manifest["preview_image"] = preview_file
        
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return manifest_path
