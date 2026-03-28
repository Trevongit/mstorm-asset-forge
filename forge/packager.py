import json
import os
import datetime
import uuid

def create_asset_package(output_root, asset_name, primitive, scale, version="1.0.0"):
    """
    Creates a standardized package directory and manifest.json.
    """
    timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"{timestamp_folder}_{asset_name}"
    package_path = os.path.join(output_root, package_name)
    os.makedirs(package_path, exist_ok=True)
    
    # Precise UTC timestamp for manifest
    manifest_timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    asset_id = str(uuid.uuid4())
    
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
        "tags": ["generated", "mvp", "prop", primitive]
    }
    
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return package_path, manifest_path
