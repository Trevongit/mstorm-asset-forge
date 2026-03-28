import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), output_path="asset.obj"):
    """
    Generates a minimal Blender Python script to create a primitive and export it as OBJ.
    """
    # Map primitives to Blender ops
    primitive_map = {
        "cube": "bpy.ops.mesh.primitive_cube_add",
        "sphere": "bpy.ops.mesh.primitive_uv_sphere_add",
        "cylinder": "bpy.ops.mesh.primitive_cylinder_add",
        "plane": "bpy.ops.mesh.primitive_plane_add"
    }
    
    op = primitive_map.get(primitive.lower(), "bpy.ops.mesh.primitive_cube_add")
    
    # We use os.path.abspath to ensure Blender writes to the correct location
    abs_output_path = os.path.abspath(output_path)
    
    script = f"""
import bpy
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create the primitive
{op}(location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "{asset_name}"

# Apply scale
obj.scale = ({scale[0]}, {scale[1]}, {scale[2]})
bpy.ops.object.transform_apply(scale=True)

# Export to OBJ (Baseline Format)
print(f"Blender: Exporting to {{'{abs_output_path}'}}")
if hasattr(bpy.ops.wm, 'obj_export'):
    bpy.ops.wm.obj_export(filepath='{abs_output_path}', export_selected_objects=True)
else:
    bpy.ops.export_scene.obj(filepath='{abs_output_path}', use_selection=True)

print(f"Blender: Successfully exported {{obj.name}}")
"""
    return textwrap.dedent(script).strip()
