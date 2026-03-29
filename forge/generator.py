import textwrap
import os

PRESETS = {
    "chair_basic": {
        "primitive": "chair",
        "description": "Standard four-legged chair with backrest",
        "bpy_code": """
# Chair Assembly
# Seat
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
seat = bpy.context.active_object
seat.scale = (0.5, 0.5, 0.05)

# Legs
leg_coords = [(0.4, 0.4, 0.25), (0.4, -0.4, 0.25), (-0.4, 0.4, 0.25), (-0.4, -0.4, 0.25)]
for lx, ly, lz in leg_coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.5, location=(lx, ly, lz))
    bpy.context.active_object.parent = seat

# Backrest
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.45, 0, 1.0))
back = bpy.context.active_object
back.scale = (0.05, 0.5, 0.5)
back.parent = seat

bpy.context.view_layer.objects.active = seat
bpy.ops.object.select_all(action='DESELECT')
seat.select_set(True)
for child in seat.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "chair_dining": {
        "primitive": "chair",
        "description": "Slimmer dining chair with taller back",
        "bpy_code": """
# Dining Chair Assembly
# Seat
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.6))
seat = bpy.context.active_object
seat.scale = (0.45, 0.45, 0.04)

# Taller Legs
leg_coords = [(0.38, 0.38, 0.3), (0.38, -0.38, 0.3), (-0.38, 0.38, 0.3), (-0.38, -0.38, 0.3)]
for lx, ly, lz in leg_coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.6, location=(lx, ly, lz))
    bpy.context.active_object.parent = seat

# Tall Slim Backrest
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.4, 0, 1.2))
back = bpy.context.active_object
back.scale = (0.03, 0.4, 0.7)
back.parent = seat

bpy.context.view_layer.objects.active = seat
bpy.ops.object.select_all(action='DESELECT')
seat.select_set(True)
for child in seat.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "bench_basic": {
        "primitive": "bench",
        "description": "Simple wide bench",
        "bpy_code": """
# Bench Assembly
# Seat
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.45))
seat = bpy.context.active_object
seat.scale = (0.4, 1.2, 0.05)

# 4 Legs
leg_coords = [(0.3, 1.0, 0.225), (0.3, -1.0, 0.225), (-0.3, 1.0, 0.225), (-0.3, -1.0, 0.225)]
for lx, ly, lz in leg_coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.45, location=(lx, ly, lz))
    bpy.context.active_object.parent = seat

bpy.context.view_layer.objects.active = seat
bpy.ops.object.select_all(action='DESELECT')
seat.select_set(True)
for child in seat.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "cabinet_basic": {
        "primitive": "cabinet",
        "description": "Simple box cabinet with door detail",
        "bpy_code": """
# Cabinet Assembly
# Main Body
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
body = bpy.context.active_object
body.scale = (0.4, 0.8, 1.0)

# Door Insets (Visual suggestion)
# Left Door
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.41, 0.19, 0.5))
door_l = bpy.context.active_object
door_l.scale = (0.01, 0.35, 0.95)
door_l.parent = body

# Right Door
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.41, -0.19, 0.5))
door_r = bpy.context.active_object
door_r.scale = (0.01, 0.35, 0.95)
door_r.parent = body

bpy.context.view_layer.objects.active = body
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
for child in body.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "dining_table_basic": {
        "primitive": "table",
        "description": "Large dining table",
        "bpy_code": """
# Dining Table Assembly
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.75))
top = bpy.context.active_object
top.scale = (1.0, 0.5, 0.05) # 2m x 1m top

leg_coords = [(0.9, 0.4, 0.375), (0.9, -0.4, 0.375), (-0.9, 0.4, 0.375), (-0.9, -0.4, 0.375)]
for lx, ly, lz in leg_coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.75, location=(lx, ly, lz))
    bpy.context.active_object.parent = top

bpy.context.view_layer.objects.active = top
bpy.ops.object.select_all(action='DESELECT')
top.select_set(True)
for child in top.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "table_round": {
        "primitive": "table",
        "description": "Round table with center pedestal",
        "bpy_code": """
# Round Table Assembly
# Top
bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=0.05, location=(0, 0, 0.75))
top = bpy.context.active_object

# Center Pedestal
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.7, location=(0, 0, 0.35))
pedestal = bpy.context.active_object
pedestal.parent = top

# Base Plate
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.05, location=(0, 0, 0.025))
base = bpy.context.active_object
base.parent = top

bpy.context.view_layer.objects.active = top
bpy.ops.object.select_all(action='DESELECT')
top.select_set(True)
for child in top.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "pillar_square": {
        "primitive": "pillar",
        "description": "Architectural square pillar",
        "bpy_code": """
# Pillar Assembly
# Base
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.1))
base = bpy.context.active_object
base.scale = (0.4, 0.4, 0.1)

# Shaft
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.1))
shaft = bpy.context.active_object
shaft.scale = (0.3, 0.3, 0.9)
shaft.parent = base

# Capital
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.1))
capital = bpy.context.active_object
capital.scale = (0.4, 0.4, 0.1)
capital.parent = base

bpy.context.view_layer.objects.active = base
bpy.ops.object.select_all(action='DESELECT')
base.select_set(True)
for child in base.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "shelf_simple": {
        "primitive": "shelf",
        "description": "Basic multi-tier shelf",
        "bpy_code": """
# Shelf Assembly
# Sides
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.5, 1.0))
side_l = bpy.context.active_object
side_l.scale = (0.4, 0.05, 1.0)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.5, 1.0))
side_r = bpy.context.active_object
side_r.scale = (0.4, 0.05, 1.0)
side_r.parent = side_l

# Shelves
heights = [0.2, 0.9, 1.6]
for h in heights:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, h))
    s = bpy.context.active_object
    s.scale = (0.4, 0.45, 0.03)
    s.parent = side_l

bpy.context.view_layer.objects.active = side_l
bpy.ops.object.select_all(action='DESELECT')
side_l.select_set(True)
for child in side_l.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "crate_stackable": {
        "primitive": "crate",
        "description": "Reinforced stackable crate",
        "bpy_code": """
# Stackable Crate
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
base = bpy.context.active_object
base.scale = (0.5, 0.5, 0.5)

# Corner posts for "stackable" feel
coords = [(0.45, 0.45, 0.5), (0.45, -0.45, 0.5), (-0.45, 0.45, 0.5), (-0.45, -0.45, 0.5)]
for lx, ly, lz in coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=1.1, location=(lx, ly, lz))
    bpy.context.active_object.parent = base

bpy.context.view_layer.objects.active = base
bpy.ops.object.select_all(action='DESELECT')
base.select_set(True)
for child in base.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    },
    "stool_round": {
        "primitive": "stool",
        "description": "Round stool preset",
        "bpy_code": """
# Stool Assembly
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.1, location=(0, 0, 0.5))
seat = bpy.context.active_object

leg_coords = [(0.3, 0.3, 0.25), (0.3, -0.3, 0.25), (-0.3, 0.3, 0.25), (-0.3, -0.3, 0.25)]
for lx, ly, lz in leg_coords:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.5, location=(lx, ly, lz))
    bpy.context.active_object.parent = seat

bpy.context.view_layer.objects.active = seat
bpy.ops.object.select_all(action='DESELECT')
seat.select_set(True)
for child in seat.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    }
}

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), 
                        shading="flat", bevel=0.0, subdivisions=0, 
                        auto_smooth=False, base_color=(0.8, 0.8, 0.8), 
                        metallic=0.0, roughness=0.5,
                        emission_color=(0.0, 0.0, 0.0), emission_strength=0.0,
                        alpha=1.0, material_name="ForgeMaterial",
                        output_path="asset.obj", preview_path=None, 
                        export_format="obj", python_code=None,
                        preset_name=None):
    """
    Generates a minimal Blender Python script to create geometry (primitives or modular props), 
    apply PBR materials and modifiers, render a preview, and export.
    """
    abs_output_path = os.path.abspath(output_path)
    abs_preview_path = os.path.abspath(preview_path) if preview_path else ""
    
    shading_cmd = "bpy.ops.object.shade_smooth()" if shading.lower() == "smooth" else "bpy.ops.object.shade_flat()"

    # Geometry Generation Block
    if python_code:
        geo_gen = python_code
    elif preset_name and preset_name in PRESETS:
        geo_gen = PRESETS[preset_name]["bpy_code"]
    elif primitive.lower() == "table":
        geo_gen = """
# Table Assembly (Top + 4 Legs)
# Top
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.9))
top = bpy.context.active_object
top.scale = (1.5, 1.0, 0.1)

# Legs
leg_coords = [(1.3, 0.8, 0.45), (1.3, -0.8, 0.45), (-1.3, 0.8, 0.45), (-1.3, -0.8, 0.45)]
for i, (lx, ly, lz) in enumerate(leg_coords):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.9, location=(lx, ly, lz))
    leg = bpy.context.active_object
    leg.parent = top
    
bpy.context.view_layer.objects.active = top
bpy.ops.object.select_all(action='DESELECT')
top.select_set(True)
for child in top.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    elif primitive.lower() == "stool":
        geo_gen = """
# Stool Assembly (Seat + 4 Legs)
# Seat
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=0.1, location=(0, 0, 0.5))
seat = bpy.context.active_object

# Legs
leg_coords = [(0.3, 0.3, 0.25), (0.3, -0.3, 0.25), (-0.3, 0.3, 0.25), (-0.3, -0.3, 0.25)]
for i, (lx, ly, lz) in enumerate(leg_coords):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.5, location=(lx, ly, lz))
    leg = bpy.context.active_object
    leg.parent = seat
    
bpy.context.view_layer.objects.active = seat
bpy.ops.object.select_all(action='DESELECT')
seat.select_set(True)
for child in seat.children:
    child.select_set(True)
bpy.ops.object.join()
obj = bpy.context.active_object
"""
    elif primitive.lower() == "crate":
        geo_gen = """
# Crate Assembly (Solid box with frame-ready topology)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
obj = bpy.context.active_object
"""
    else:
        # Standard Primitives
        primitive_map = {
            "cube": "bpy.ops.mesh.primitive_cube_add",
            "sphere": "bpy.ops.mesh.primitive_uv_sphere_add",
            "cylinder": "bpy.ops.mesh.primitive_cylinder_add",
            "plane": "bpy.ops.mesh.primitive_plane_add"
        }
        op = primitive_map.get(primitive.lower(), "bpy.ops.mesh.primitive_cube_add")
        geo_gen = f"{op}(location=(0, 0, 0))\nobj = bpy.context.active_object"

    # Material inputs
    color_repr = f"'{base_color}'" if isinstance(base_color, str) else str(base_color)
    emit_color_repr = f"'{emission_color}'" if isinstance(emission_color, str) else str(emission_color)

    script = f"""import bpy
import os
import json
import math
from mathutils import Vector

def hex_to_rgb(hex_str):
    if not isinstance(hex_str, str): return hex_str
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0
    return (r, g, b, 1.0)

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

# --- Material Setup (PBR) ---
mat = bpy.data.materials.new(name="{material_name}")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")

if principled:
    # Base Color & Alpha
    bc = {color_repr}
    bc_rgba = hex_to_rgb(bc) if isinstance(bc, str) else (bc[0], bc[1], bc[2], 1.0)
    principled.inputs['Base Color'].default_value = bc_rgba
    principled.inputs['Alpha'].default_value = {alpha}
    
    # Metal / Rough
    principled.inputs['Metallic'].default_value = {metallic}
    principled.inputs['Roughness'].default_value = {roughness}
    
    # Emission
    ec = {emit_color_repr}
    ec_rgba = hex_to_rgb(ec) if isinstance(ec, str) else (ec[0], ec[1], ec[2], 1.0)
    principled.inputs['Emission Color'].default_value = ec_rgba
    principled.inputs['Emission Strength'].default_value = {emission_strength}

    # Blend Mode for Transparency
    if {alpha} < 1.0:
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'HASHED'

if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

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

# --- Geometry Stats & Dimensions ---
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
mesh_eval = obj_eval.to_mesh()

v_count = len(mesh_eval.vertices)
f_count = len(mesh_eval.polygons)

# Calculate world-space dimensions
bbox = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
min_coords = Vector((min(c.x for c in bbox), min(c.y for c in bbox), min(c.z for c in bbox)))
max_coords = Vector((max(c.x for c in bbox), max(c.y for c in bbox), max(c.z for c in bbox)))
dims = max_coords - min_coords

stats = {{
    "vertex_count": v_count, 
    "face_count": f_count,
    "dimensions": {{
        "x": round(dims.x, 3),
        "y": round(dims.y, 3),
        "z": round(dims.z, 3)
    }}
}}
print("FORGE_STATS: " + json.dumps(stats))

# --- Preview Rendering ---
if "{abs_preview_path}":
    print("Blender: Setting up adaptive preview render...")
    center = sum(bbox, Vector()) / 8
    dims_v = obj_eval.dimensions
    max_dim = max(dims_v.x, dims_v.y, dims_v.z, 0.1)
    
    cam_dist = max_dim * 3.5
    cam_loc = center + Vector((cam_dist, -cam_dist, cam_dist * 0.8))
    
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
    
    try:
        bpy.ops.render.render(write_still=True)
        print("Blender: Preview render SUCCESS.")
    except Exception as e:
        print("Blender: Preview render FAILED: " + str(e))

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
