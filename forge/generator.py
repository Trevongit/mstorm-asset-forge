import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), output_path="asset.obj", preview_path=None):
    """
    Generates a minimal Blender Python script to create a primitive, 
    render a preview, and export it as OBJ.
    """
    # Map primitives to Blender ops
    primitive_map = {
        "cube": "bpy.ops.mesh.primitive_cube_add",
        "sphere": "bpy.ops.mesh.primitive_uv_sphere_add",
        "cylinder": "bpy.ops.mesh.primitive_cylinder_add",
        "plane": "bpy.ops.mesh.primitive_plane_add"
    }
    
    op = primitive_map.get(primitive.lower(), "bpy.ops.mesh.primitive_cube_add")
    
    abs_output_path = os.path.abspath(output_path)
    
    # Optional rendering logic
    render_logic = ""
    if preview_path:
        abs_preview_path = os.path.abspath(preview_path)
        render_logic = f"""
# --- Preview Rendering ---
print("Blender: Setting up preview render...")
# Setup Camera
bpy.ops.object.camera_add(location=(7.0, -7.0, 5.0), rotation=(1.1, 0, 0.785))
bpy.context.scene.camera = bpy.context.active_object

# Setup Light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
bpy.context.active_object.data.energy = 5.0

# Render settings (Eevee baseline)
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = '{abs_preview_path}'
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 100

print(f"Blender: Rendering preview to {{'{abs_preview_path}'}}")
try:
    bpy.ops.render.render(write_still=True)
    print("Blender: Preview render SUCCESS.")
except Exception as e:
    print(f"Blender: Preview render FAILED: {{e}}")
"""

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

{render_logic}

# --- Export ---
print(f"Blender: Exporting to {{'{abs_output_path}'}}")
if hasattr(bpy.ops.wm, 'obj_export'):
    bpy.ops.wm.obj_export(filepath='{abs_output_path}', export_selected_objects=True)
else:
    bpy.ops.export_scene.obj(filepath='{abs_output_path}', use_selection=True)

print(f"Blender: Successfully exported {{obj.name}}")
"""
    return textwrap.dedent(script).strip()
