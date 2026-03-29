import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), 
                        shading="flat", bevel=0.0, subdivisions=0, 
                        auto_smooth=False, output_path="asset.obj", 
                        preview_path=None, export_format="obj",
                        python_code=None):
    """
    Generates a minimal Blender Python script to create geometry, 
    apply modifiers, render an adaptive preview, and export it as OBJ or GLB.
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
    abs_preview_path = os.path.abspath(preview_path) if preview_path else ""
    
    shading_cmd = "bpy.ops.object.shade_smooth()" if shading.lower() == "smooth" else "bpy.ops.object.shade_flat()"

    # Geometry Generation Block - no leading indent here
    if python_code:
        geo_gen = python_code
    else:
        geo_gen = f"{op}(location=(0, 0, 0))\nobj = bpy.context.active_object"

    # We use a simple concatenation/formatting to avoid complex dedent logic
    script = f"""import bpy
import os
import json
import math
from mathutils import Vector

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- Geometry Generation ---
{geo_gen}

obj = bpy.context.active_object
obj.name = "{asset_name}"

# Apply scale
obj.scale = ({scale[0]}, {scale[1]}, {scale[2]})
bpy.ops.object.transform_apply(scale=True)

# --- Apply Modifiers ---
if {bevel} > 0:
    bev = obj.modifiers.new(name="ForgeBevel", type='BEVEL')
    bev.width = {bevel}
    bev.segments = 3
    
if {subdivisions} > 0:
    sub = obj.modifiers.new(name="ForgeSubsurf", type='SUBSURF')
    sub.levels = {subdivisions}
    sub.render_levels = {subdivisions}

# Apply shading
{shading_cmd}

if {"True" if auto_smooth else "False"}:
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599 # 30 degrees

# --- Geometry Stats Extraction (Evaluated) ---
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
mesh_eval = obj_eval.to_mesh()

v_count = len(mesh_eval.vertices)
f_count = len(mesh_eval.polygons)
stats = {{"vertex_count": v_count, "face_count": f_count}}
print("FORGE_STATS: " + json.dumps(stats))

# --- Preview Rendering (Adaptive) ---
if "{abs_preview_path}":
    print("Blender: Setting up adaptive preview render...")
    
    bbox = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
    center = sum(bbox, Vector()) / 8
    dims = obj_eval.dimensions
    max_dim = max(dims.x, dims.y, dims.z, 0.1)
    
    cam_dist = max_dim * 3.0
    cam_loc = center + Vector((cam_dist, -cam_dist, cam_dist * 0.7))
    
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam
    
    direction = center - cam.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()
    
    bpy.ops.object.light_add(type='SUN', location=cam_loc + Vector((0, 0, cam_dist)))
    bpy.context.active_object.data.energy = 5.0
    
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = "{abs_preview_path}"
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.resolution_percentage = 100
    
    try:
        bpy.ops.render.render(write_still=True)
        print("Blender: Preview render SUCCESS.")
    except Exception as e:
        print("Blender: Preview render FAILED: " + str(e))

# Cleanup mesh
obj_eval.to_mesh_clear()

# --- Export ---
print("Blender: Exporting to {abs_output_path}")
if "{export_format.lower()}" == "glb":
    bpy.ops.export_scene.gltf(
        filepath="{abs_output_path}",
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_yup=True
    )
else:
    if hasattr(bpy.ops.wm, 'obj_export'):
        bpy.ops.wm.obj_export(filepath="{abs_output_path}", export_selected_objects=True)
    else:
        bpy.ops.export_scene.obj(filepath="{abs_output_path}", use_selection=True)

print("Blender: Successfully exported " + obj.name)
"""
    return script.strip()
