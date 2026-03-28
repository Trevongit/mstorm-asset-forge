# MStorm Asset Forge — Package Contract (MVP v0.1)

This document formalizes the input, output, and behavior contracts for the MStorm Asset Forge.

## 1. Versioning
*   **Contract Version:** MVP v0.1
*   **Primary Export Baseline:** OBJ/MTL
*   **Status:** Stable for Static Props

---

## 2. Input Contract (Request JSON Schema)

The Forge accepts a JSON file via the `--file` flag.

### Schema
```json
{
  "asset": {
    "name": "string (Required)",
    "primitive": "cube|sphere|cylinder|plane (Required)",
    "scale": [float, float, float] (Optional, default [1.0, 1.0, 1.0])
  },
  "options": {
    "no_preview": boolean (Optional, default false),
    "output_dir": "string (Optional, default 'outputs')",
    "tags": ["string", ...] (Optional)
  }
}
```

### Validation Rules
*   **Hard Fail:** Missing `asset.name` or `asset.primitive` in JSON.
*   **Hard Fail:** Invalid JSON syntax.
*   **Precedence:** CLI flags (e.g., `--name`) explicitly override values in the JSON file.

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
  "generator": "MStorm Asset Forge v0.1",
  "timestamp": "ISO-8601-UTC",
  "metadata": {
    "primitive": "primitive_type",
    "scale": [x, y, z],
    "unit_system": "metric",
    "is_rigged": false
  },
  "tags": ["base_tags", "user_tags", ...],
  "preview_image": "preview.png (Optional)"
}
```

---

## 4. Operational Behavior
*   **Unit System:** All scales and measurements are in **Metric (Meters)**.
*   **Preview Failure:** If OBJ/MTL export succeeds but `preview.png` rendering fails, the package is considered **SUCCESSFUL**, and the `preview_image` field is omitted from the manifest.
*   **Blender Version:** Orchestrated via Blender 4.0.2 in headless mode.
*   **Format Limitation:** glTF/GLB export is currently excluded from this contract due to system-level library constraints.
