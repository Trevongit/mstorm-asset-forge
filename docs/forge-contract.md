# MStorm Asset Forge — Package Contract (MVP v0.1)

This document formalizes the input, output, and behavior contracts for the MStorm Asset Forge.

## 1. Versioning
*   **Contract Version:** MVP v0.1
*   **Primary Export Baselines:** OBJ/MTL, GLB
*   **Status:** Stable for Static Props

---

## 2. Input Contract (Request JSON Schema)

The Forge accepts a JSON file via the `--file` flag. It supports two root shapes: **Single Request** (Object) and **Batch Request** (List).

### Single Request Schema (Object)
```json
{
  "asset": {
    "name": "string (Required)",
    "primitive": "cube|sphere|cylinder|plane (Required for standard mode)",
    "scale": [float, float, float] (Optional, default [1.0, 1.0, 1.0])
  },
  "options": {
    "format": "obj|glb (Optional, default 'obj')",
    "category": "string (Optional, e.g., 'furniture')",
    "zip": "boolean (Optional, default false)",
    "shading": "flat|smooth (Optional, default 'flat')",
    "base_color": "string (Hex #RRGGBB) | [r, g, b] (Optional, default #CCCCCC)",
    "metallic": "float (0.0 - 1.0, Optional, default 0.0)",
    "roughness": "float (0.0 - 1.0, Optional, default 0.5)",
    "bevel": "float (Optional, non-negative, default 0.0)",
    "subdivisions": "int (Optional, 0-5, default 0)",
    "auto_smooth": "boolean (Optional, default false)",
    "python_code": "string (Optional, experimental, used in sandbox mode)",
    "author": "string (Optional, default 'MStorm Forge')",
    "no_preview": boolean (Optional, default false),
    "output_dir": "string (Optional, default 'outputs')",
    "tags": ["string", ...] (Optional)
  }
}
```

---

## 3. Output Contract (Package Structure)

The Forge produces a timestamped directory containing the following artifacts:

### Package Folder Tree
```text
outputs/
├── registry.json       # Global library index (Latest-only upsert)
├── <package_name>.zip  # Compressed package (if zip=true)
└── <YYYYMMDD_HHMMSS>_<asset_name>/
    ├── asset.obj       # The 3D model (if format=obj)
    ├── asset.mtl       # Associated material library (if format=obj)
    ├── asset.glb       # The 3D model (if format=glb)
    ├── manifest.json   # Asset metadata (Required)
    └── preview.png     # Rendered preview (Optional, non-fatal)
```

### Manifest Schema (`manifest.json`)
```json
{
  "asset_id": "uuid-v4",
  "name": "asset_name",
  "type": "static_prop",
  "format": "obj|glb",
  "entry_point": "asset.ext",
  "version": "1.0.0",
  "author": "author_name",
  "generator": "MStorm Asset Forge v0.1",
  "timestamp": "ISO-8601-UTC",
  "metadata": {
    "primitive": "primitive_type",
    "scale": [x, y, z],
    "unit_system": "metric",
    "is_rigged": false,
    "parametric_options": {
        "base_color": "string|list",
        "metallic": float,
        "roughness": float,
        "bevel": float,
        "subdivisions": int,
        "auto_smooth": boolean,
        "shading": "flat|smooth"
    }
  }
}
```

---

## 4. Operational Behavior
*   **Unit System:** All scales and measurements are in **Metric (Meters)**.
*   **PBR Materials:** The Forge uses a standard **Blender Principled BSDF** material.
    *   **GLB Path:** Supports full PBR (Color, Metal, Rough).
    *   **OBJ Path:** Primarily supports Color (Diffuse); Metallic and Roughness may not be accurately represented in MTL.
*   **Experimental Sandbox Mode:** Triggered via `--prompt-to-bpy`. Allows LLM-generated code snippets for geometry generation only.
*   **Blender Version:** Orchestrated via Blender 4.0.2 in headless mode.
