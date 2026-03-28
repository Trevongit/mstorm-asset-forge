import bpy
import os

# 1. Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Create simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "ProofCube"

# 3. Predictable output path
output_path = os.path.abspath("proof_output.glb")

# 4. Export GLB
print(f"Attempting GLB export to: {output_path}")
try:
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        use_selection=True
    )
    print("GLB_EXPORT_SUCCESS")
except Exception as e:
    print(f"GLB_EXPORT_FAILED: {e}")
