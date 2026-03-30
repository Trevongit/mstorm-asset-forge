# MStorm Asset Forge — Package Contract (MVP v0.1)

This document formalizes the input, output, and behavior contracts for the MStorm Asset Forge.

## 1. Versioning
*   **Contract Version:** MVP v0.1
*   **Primary Export Baselines:** OBJ/MTL, GLB
*   **Status:** Stable for Static Props & Modular Assemblies

---

## 2. Input Contract (Request JSON Schema)

The Forge accepts a JSON file via the `--file` flag. It supports two root shapes: **Single Request** (Object) and **Batch Request** (List).

### Single Request Schema (Object)
```json
{
  "asset": {
    "name": "string (Required)",
    "primitive": "cube|sphere|cylinder|plane|table|stool|crate (Required for standard mode)",
    "scale": [float, float, float] (Optional, default [1.0, 1.0, 1.0])
  },
  "options": {
    "preset": "chair_basic|chair_dining|bench_basic|cabinet_basic|dining_table_basic|table_round|pillar_square|shelf_simple|crate_stackable|stool_round (Optional)",
    "format": "obj|glb (Optional, default 'obj')",
    "category": "string (Optional, e.g., 'furniture')",
    "zip": "boolean (Optional, default false)",
    "validation_profile": "mobile|standard|high_fidelity (Optional, default 'standard')",
    "shading": "flat|smooth (Optional, default 'flat')",
    "base_color": "string (Hex #RRGGBB) | [r, g, b] (Optional, default #CCCCCC)",
    "metallic": "float (0.0 - 1.0, Optional, default 0.0)",
    "roughness": "float (0.0 - 1.0, Optional, default 0.5)",
    "emission_color": "string (Hex #RRGGBB) (Optional, default #000000)",
    "emission_strength": "float (>= 0.0, Optional, default 0.0)",
    "alpha": "float (0.0 - 1.0, Optional, default 1.0)",
    "material_name": "string (Optional, default 'ForgeMaterial')",
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

The Forge produces a timestamped directory and updates a global library registry.

### Package Folder Tree
```text
outputs/
├── registry.json       # Enriched Library Index (Discovery Layer)
├── <package_name>.zip  # Compressed package (if zip=true)
└── <YYYYMMDD_HHMMSS>_<asset_name>/
    ├── asset.obj       # The 3D model (if format=obj)
    ├── asset.mtl       # Associated material library (if format=obj)
    ├── asset.glb       # The 3D model (if format=glb)
    ├── manifest.json   # Detailed Asset Metadata (Truth Layer)
    └── preview.png     # Rendered preview (Optional, non-fatal)
```

### Registry Responsibilities (`registry.json`)
The registry is the **discovery layer**, optimized for fast scanning and external bridge consumption.
*   **Enriched Fields:** `validation_profile`, `dimensions_bbox_m` (WxDxH), `material_summary` (base_color, metallic, roughness, alpha, emission, material_name), `preset_name`, `has_preview`, and `has_archive`.
*   **Logical Keys:** Assets are uniquely indexed by `name|category|format`.
*   **Usage:** External tools should scan the registry first to locate assets and resolve paths.

### Manifest Responsibilities (`manifest.json`)
The manifest is the **detailed truth layer**, containing the full technical history of the asset.
*   **Content:** Full provenance, detailed geometry stats, full validation reports, and raw deterministic input parameters.
*   **Usage:** Consumers should read the manifest only when deep technical inspection or re-generation is required.

---

## 4. Operational Behavior
*   **Unit System:** All scales and measurements are in **Metric (Meters)**.
*   **Modular Props & Presets:** 
    *   Presets (e.g., `chair_basic`) are deterministic recipes that resolve to compound assemblies.
    *   *Scale:* Applied to the entire assembly after grouping.
*   **Validation Profiles:**
    *   `mobile`: 10k faces / 10MB limit. GLB preferred.
    *   `standard`: 50k faces / 50MB limit.
    *   `high_fidelity`: 250k faces / 250MB limit.
*   **PBR Materials:** Standard Blender Principled BSDF.
    *   **GLB Path:** Full PBR support (Color, Alpha, Metal, Rough, Emission).
*   **Blender Version:** Orchestrated via Blender 4.0.2 in headless mode.
