import textwrap
import os

def generate_bpy_script(asset_name, primitive="cube", scale=(1.0, 1.0, 1.0), shading="flat", output_path="asset.obj", preview_path=None):
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
    abs_preview_path = os.path.abspath(preview_path) if preview_path else ""
    
    shading_cmd = "bpy.ops.object.shade_smooth()" if shading.lower() == "smooth" else "bpy.ops.object.shade_flat()"

    # We build the script using string formatting instead of a giant f-string to avoid escaping issues
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

        # Apply shading
        {shading_cmd}

        # --- Geometry Stats Extraction ---
        v_count = len(obj.data.vertices)
        f_count = len(obj.data.polygons)
        stats = {{"vertex_count": v_count, "face_count": f_count}}
        print("FORGE_STATS: " + json.dumps(stats))

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
            bpy.ops.wm.obj_export(filepath="{output_path}", export_selected_objects=True)
        else:
            bpy.ops.export_scene.obj(filepath="{output_path}", use_selection=True)

        print("Blender: Successfully exported " + obj.name)
    """).strip()

    return script_template.format(
        op=op,
        asset_name=asset_name,
        scale_x=scale[0],
        scale_y=scale[1],
        scale_z=scale[2],
        shading_cmd=shading_cmd,
        preview_path=abs_preview_path,
        output_path=abs_output_path
    )
