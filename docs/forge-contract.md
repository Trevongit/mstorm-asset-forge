# MStorm Asset Forge — Package Contract (MVP v0.1)

This document formalizes the input, output, and behavior contracts for the MStorm Asset Forge.

## 1. Versioning
*   **Contract Version:** MVP v0.1
*   **Primary Export Baseline:** OBJ/MTL
*   **Status:** Stable for Static Props

---

## 2. Input Contract (Request JSON Schema)

The Forge accepts a JSON file via the `--file` flag. It supports two root shapes: **Single Request** (Object) and **Batch Request** (List).

### Single Request Schema (Object)
```json
{
  "asset": {
    "name": "string (Required)",
    "primitive": "cube|sphere|cylinder|plane (Required)",
    "scale": [float, float, float] (Optional, default [1.0, 1.0, 1.0])
  },
  "options": {
    "shading": "flat|smooth (Optional, default 'flat')",
    "bevel": "float (Optional, non-negative, default 0.0)",
    "subdivisions": "int (Optional, 0-5, default 0)",
    "auto_smooth": "boolean (Optional, default false)",
    "author": "string (Optional, default 'MStorm Forge')",
    "no_preview": boolean (Optional, default false),
    "output_dir": "string (Optional, default 'outputs')",
    "tags": ["string", ...] (Optional)
  }
}
```

### Batch Request Schema (List)
A JSON list where each element follows the **Single Request Schema** structure.
```json
[
  { "asset": { "name": "item1", "primitive": "cube" } },
  { "asset": { "name": "item2", "primitive": "sphere" } }
]
```

### Validation Rules
*   **Hard Fail:** Missing `asset.name` or `asset.primitive` in JSON (for single mode).
*   **Batch Behavior:** If an item in a batch fails, the Forge logs the error and continues to the next item. The process returns a non-zero exit code if any item failed.
*   **Precedence:** CLI flags explicitly override values in the JSON file. In batch mode, specific CLI overrides (e.g., `--no-preview`, `--output-dir`, `--author`) are applied globally to all items.

---

## 3. Output Contract (Package Structure)

The Forge produces a timestamped directory containing the following artifacts:

### Package Folder Tree
```text
outputs/
└── <YYYYMMDD_HHMMSS>_<asset_name>/
    ├── asset.obj       # The 3D model (OBJ format)
    ├── asset.mtl       # Associated material library
    ├── manifest.json   # Asset metadata (Required)
    └── preview.png     # Rendered preview (Optional, non-fatal)
```

### Manifest Schema (`manifest.json`)
```json
{
  "asset_id": "uuid-v4",
  "name": "asset_name",
  "type": "static_prop",
  "format": "obj",
  "version": "1.0.0",
  "author": "author_name",
  "generator": "MStorm Asset Forge v0.1",
  "timestamp": "ISO-8601-UTC",
  "provenance": {
    "source_type": "primitive",
    "creation_command": "reproducible_command_string"
  },
  "metadata": {
    "primitive": "primitive_type",
    "scale": [x, y, z],
    "unit_system": "metric",
    "unit_scale": "1.0 unit = 1.0 meter",
    "is_rigged": false
  },
  "tags": ["base_tags", "user_tags", ...],
  "preview_image": "preview.png (Optional)"
}
```

---

## 4. Operational Behavior
*   **Unit System:** All scales and measurements are in **Metric (Meters)**.
*   **Modifier Behavior:** Parametric modifiers are applied sequentially (Bevel then Subdivision). 
    *   *Note:* Applying `bevel` or `subdivisions` to a zero-thickness `plane` may result in little to no visible geometry change in the output.
*   **Preview Failure:** If OBJ/MTL export succeeds but `preview.png` rendering fails, the package is considered **SUCCESSFUL**, and the `preview_image` field is omitted from the manifest.
*   **Blender Version:** Orchestrated via Blender 4.0.2 in headless mode.
*   **Format Limitation:** glTF/GLB export is currently excluded from this contract due to system-level library constraints.
