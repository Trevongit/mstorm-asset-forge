import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), 
                        shading="flat", bevel=0.0, subdivisions=0, 
                        auto_smooth=False, output_path="asset.obj", 
                        preview_path=None):
    """
    Generates a minimal Blender Python script to create a primitive, 
    apply modifiers, render a preview, and export it as OBJ.
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
        
        # 1. Bevel
        if {bevel} > 0:
            bev = obj.modifiers.new(name="ForgeBevel", type='BEVEL')
            bev.width = {bevel}
            # Optional: ensure segments are reasonable
            bev.segments = 3
            
        # 2. Subdivisions
        if {subdivisions} > 0:
            sub = obj.modifiers.new(name="ForgeSubsurf", type='SUBSURF')
            sub.levels = {subdivisions}
            sub.render_levels = {subdivisions}

        # Apply shading
        {shading_cmd}
        
        # 3. Auto Smooth (Specific to Blender 4.0.2 handling)
        if {auto_smooth}:
            # In 4.0, shade_smooth with auto_smooth is often handled via mesh property
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = 0.523599 # 30 degrees

        # --- Geometry Stats Extraction ---
        # Note: We use evaluated mesh to get counts after modifiers
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        
        v_count = len(mesh_eval.vertices)
        f_count = len(mesh_eval.polygons)
        stats = {{"vertex_count": v_count, "face_count": f_count}}
        print("FORGE_STATS: " + json.dumps(stats))
        
        obj_eval.to_mesh_clear()

        # --- Preview Rendering ---
        if "{preview_path}":
            print("Blender: Setting up preview render...")
            bpy.ops.object.camera_add(location=(7.0, -7.0, 5.0), rotation=(1.1, 0, 0.785))
            bpy.context.scene.camera = bpy.context.active_object
            bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
            bpy.context.active_object.data.energy = 5.0
            
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
