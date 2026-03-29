import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), 
                        shading="flat", bevel=0.0, subdivisions=0, 
                        auto_smooth=False, output_path="asset.obj", 
                        preview_path=None):
    """
    Generates a minimal Blender Python script to create a primitive, 
    apply modifiers, render an adaptive preview, and export it as OBJ.
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

    # We build the script using string formatting
    script_template = textwrap.dedent("""
        import bpy
        import os
        import json
        import math
        from mathutils import Vector

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        # Create the primitive
        {op}(location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = "{asset_name}"

        # Apply scale
        obj.scale = ({scale_x}, {scale_y}, {scale_z})
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
        
        if {auto_smooth}:
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
        if "{preview_path}":
            print("Blender: Setting up adaptive preview render...")
            
            # 1. Calculate Bounding Box and Extent
            # We use the evaluated object to account for modifiers
            bbox = [obj_eval.matrix_world @ Vector(corner) for corner in obj_eval.bound_box]
            center = sum(bbox, Vector()) / 8
            
            # Find max dimension for scaling
            dims = obj_eval.dimensions
            max_dim = max(dims.x, dims.y, dims.z, 0.1)
            
            # 2. Camera Setup
            # Baseline distance: 3.5x the max dimension (fits object well in 512x512)
            cam_dist = max_dim * 3.0
            # Offset the camera at an isometric-ish angle
            cam_loc = center + Vector((cam_dist, -cam_dist, cam_dist * 0.7))
            
            bpy.ops.object.camera_add(location=cam_loc)
            cam = bpy.context.active_object
            bpy.context.scene.camera = cam
            
            # Point camera at center
            direction = center - cam.location
            rot_quat = direction.to_track_quat('-Z', 'Y')
            cam.rotation_euler = rot_quat.to_euler()
            
            # 3. Light Setup
            # Position light relative to camera and object size
            bpy.ops.object.light_add(type='SUN', location=cam_loc + Vector((0, 0, cam_dist)))
            bpy.context.active_object.data.energy = 5.0
            
            # 4. Render Settings
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.filepath = "{preview_path}"
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
        print("Blender: Exporting to {output_path}")
        if hasattr(bpy.ops.wm, 'obj_export'):
            bpy.ops.wm.obj_export(filepath="{output_path}", export_selected_objects=True, apply_modifiers=True)
        else:
            bpy.ops.export_scene.obj(filepath="{output_path}", use_selection=True, use_mesh_modifiers=True)

        print("Blender: Successfully exported " + obj.name)
    """).strip()

    return script_template.format(
        op=op,
        asset_name=asset_name,
        scale_x=scale[0],
        scale_y=scale[1],
        scale_z=scale[2],
        shading_cmd=shading_cmd,
        bevel=bevel,
        subdivisions=subdivisions,
        auto_smooth="True" if auto_smooth else "False",
        preview_path=abs_preview_path,
        output_path=abs_output_path
    )
