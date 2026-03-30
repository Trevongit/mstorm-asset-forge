# MStorm Studio — Integration Guide

This guide defines the engineering contract for integrating the **MStorm Asset Forge** with external tools, automated pipelines, and MStorm Studio plugins.

## 1. Discovery-First Integration Flow

Integration must follow a two-tier discovery pattern to maintain performance and decoupling.

### Tier 1: Discovery Layer (`registry.json`)
The `outputs/registry.json` is the lightweight entry point. External tools should scan this file to populate browsers or galleries.

**Registry Responsibilities:**
*   Provide a flat, logical index of all valid assets.
*   Surface high-level metadata for filtering (`dimensions`, `validation_profile`, `material_summary`).
*   Resolve the current `package_path` for a given asset name.

### Tier 2: Truth Layer (`manifest.json`)
Read the `manifest.json` inside the specific `package_path` only when deep asset details are required (e.g., during final import or technical audit).

**Manifest Responsibilities:**
*   Store deep provenance (raw commands, LLM metadata).
*   Provide detailed geometry stats and full validation logs.
*   Maintain the definitive deterministic input contract for the asset.

---

## 2. Stable Integration Contract

To ensure long-term compatibility, external tools should rely on these stable fields in `registry.json`:
*   `name`: Logical asset identifier.
*   `format`: `glb` or `obj`.
*   `dimensions`: World-space bounding box (WxDxH) in meters.
*   `package_path`: Relative path to the asset folder.
*   `validation_success`: Global quality status flag.

---

## 3. Preferred Production Handoff

*   **Preferred Format:** `glb` (glTF Binary). This path provides the highest fidelity for PBR materials, transparency, and emission.
*   **Handoff Method:** Use the `--sync <target_path>` command. This ensures a clean mirror of the library into the project's assets directory, respecting logical overwrites.

---

## 4. What MStorm Should Not Assume

*   **Internal Folder Scraping:** Do not assume the subfolder names in `outputs/` are stable. Always resolve paths via `registry.json`.
*   **Blender Implementation:** The Forge abstracts Blender orchestration. Tools should interact only with the generated artifacts (GLB/OBJ/JSON).
*   **GUID Persistence:** While names are logical keys, `asset_id` (UUID) values are unique to each forge run.

---

## 5. Future Bridge / Plugin Direction

Future integration efforts should focus on:
*   **Live Watcher:** Monitoring `registry.json` for filesystem changes to trigger automatic re-imports.
*   **Shelf UI:** presenting the Forge registry as a visual library of ready-to-use prefabs.
*   **Metadata Propagation:** Syncing Forge tags and dimensions directly into the Studio scene database.
