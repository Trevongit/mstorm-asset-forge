import bpy
import os

# 1. Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Create simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "ProofCubeObj"

# 3. Predictable output path
output_path = os.path.abspath("proof_output.obj")

# 4. Export OBJ
# Note: In Blender 4.0+, the preferred way is often bpy.ops.wm.obj_export
# but we will use the legacy/standard export_scene if available as a baseline.
print(f"Attempting OBJ export to: {output_path}")
try:
    if hasattr(bpy.ops.wm, 'obj_export'):
        bpy.ops.wm.obj_export(filepath=output_path, export_selected_objects=True)
    else:
        bpy.ops.export_scene.obj(filepath=output_path, use_selection=True)
    print("OBJ_EXPORT_SUCCESS")
except Exception as e:
    print(f"OBJ_EXPORT_FAILED: {e}")
