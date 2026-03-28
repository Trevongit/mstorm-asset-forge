import json
import os
import datetime
import subprocess
import uuid

def generate_manifest(package_path, asset_name, primitive="cube"):
    """Creates a manifest.json file for the asset package."""
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    asset_id = str(uuid.uuid4())
    
    manifest = {
        "asset_id": asset_id,
        "name": asset_name,
        "type": "static_prop",
        "format": "obj",
        "generator": "MStorm Asset Forge Proof",
        "timestamp": timestamp,
        "metadata": {
            "primitive": primitive,
            "unit_system": "metric",
            "is_rigged": False
        },
        "tags": ["proof", "static", primitive]
    }
    
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
    return manifest_path

def run_blender_export(package_path):
    """Executes a minimal Blender script to export OBJ/MTL."""
    obj_path = os.path.join(package_path, "asset.obj")
    
    bpy_script = f"""
import bpy
import os

# Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create primitive
bpy.ops.mesh.primitive_cube_add(size=2)
obj = bpy.context.active_object
obj.name = "ProofAsset"

# Export OBJ/MTL
if hasattr(bpy.ops.wm, 'obj_export'):
    bpy.ops.wm.obj_export(filepath=os.path.abspath("{obj_path}"), export_selected_objects=True)
else:
    bpy.ops.export_scene.obj(filepath=os.path.abspath("{obj_path}"), use_selection=True)

print(f"Blender export successful to {obj_path}")
"""
    
    # Save script to temporary file
    temp_script = "temp_bpy_script.py"
    with open(temp_script, 'w') as f:
        f.write(bpy_script)
        
    # Run Blender
    try:
        cmd = ["/usr/bin/blender", "--background", "--python", temp_script]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Blender output:\n", result.stdout)
    finally:
        if os.path.exists(temp_script):
            os.remove(temp_script)

def main():
    # 1. Setup predictable package directory
    timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_dir = f"proof_package_{timestamp_folder}"
    package_path = os.path.abspath(package_dir)
    os.makedirs(package_path, exist_ok=True)
    
    print(f"Creating proof package at: {package_path}")
    
    # 2. Run Blender to generate asset.obj and asset.mtl
    run_blender_export(package_path)
    
    # 3. Generate manifest.json
    manifest_path = generate_manifest(package_path, "ProofCube", "cube")
    
    # 4. Final verification
    print("\nPackage Contents Verification:")
    for f in os.listdir(package_path):
        size = os.path.getsize(os.path.join(package_path, f))
        print(f" - {f} ({size} bytes)")
    
    print(f"\nProof Package Creation: SUCCESSFUL")

if __name__ == "__main__":
    main()
