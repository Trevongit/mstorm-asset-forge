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
    "shading": "flat|smooth (Optional, default 'flat')",
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

### Validation Rules
*   **Hard Fail:** Missing `asset.name` or `asset.primitive` in standard mode.
*   **Sandbox Safety (Experimental):** If `options.python_code` is provided, it is strictly validated. 
    *   **Blacklist:** Forbidden terms include `import`, `open`, `exec`, `eval`, `os`, `sys`, `subprocess`, etc.
    *   **Allowlist Pattern:** Snippets MUST contain geometry operators like `bpy.ops.mesh.*`.
*   **Batch Behavior:** If an item in a batch fails, the Forge logs the error and continues to the next item.

---

## 3. Output Contract (Package Structure)

The Forge produces a timestamped directory containing the following artifacts:

### Package Folder Tree
```text
outputs/
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
  "version": "1.0.0",
  "author": "author_name",
  "generator": "MStorm Asset Forge v0.1",
  "timestamp": "ISO-8601-UTC",
  "provenance": {
    "source_type": "primitive | agent_bpy_sandbox",
    "creation_command": "reproducible_command_string",
    "experimental_mode": boolean (Optional),
    "provider": "string (Optional, e.g., 'openai')",
    "model": "string (Optional, e.g., 'gpt-4o-mini')"
  },
  "metadata": {
    "primitive": "primitive_type",
    "scale": [x, y, z],
    "unit_system": "metric",
    "unit_scale": "1.0 unit = 1.0 meter",
    "is_rigged": false,
    "parametric_options": {
        "bevel": float,
        "subdivisions": int,
        "auto_smooth": boolean,
        "shading": "flat|smooth"
    }
  },
  "tags": ["base_tags", "user_tags", "experimental (if sandbox)"],
  "preview_image": "preview.png (Optional)"
}
```

---

## 4. Operational Behavior
*   **Unit System:** All scales and measurements are in **Metric (Meters)**.
*   **Experimental Sandbox Mode:** Triggered via `--prompt-to-bpy`. Allows LLM-generated code snippets for geometry generation only.
*   **Modifier Behavior:** Parametric modifiers are applied sequentially (Bevel then Subdivision) after the core geometry is created (whether by primitive or snippet).
*   **Blender Version:** Orchestrated via Blender 4.0.2 in headless mode.
*   **Format Notes:** GLB export requires `numpy` to be available in the Blender Python environment.
