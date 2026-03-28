# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**One-Day MVP: Static Prop Pipeline (OBJ Baseline).**

## What Works Right Now
*   **Orchestrator:** `main_forge.py` CLI is functional for local headless generation.
*   **Blender (4.0.2):** Verified and reachable for headless automation.
*   **OBJ/MTL Export:** Confirmed as the primary baseline format.
*   **Packager:** Automated folder + `manifest.json` generation.

## What is NOT Implemented
*   **Local Agent Strategy:** Dynamic `bpy` generation via LLM.
*   **Previews:** Automatic `preview.png` rendering.
*   **GLB Support:** Currently blocked by system-level library issues (`_ctypes`).

## Next 3 Tasks
1.  **Local Agent Integration:** Implement a local LLM/template strategy for complex geometry.
2.  **Preview Generation:** Add a Blender render pass to the forge pipeline.
3.  **Refine Manifest:** Add tags and advanced metadata to the export flow.

## Session Anchor
*   **Current Baseline Format:** OBJ/MTL.
*   **Main Entry:** `main_forge.py`.
*   **Target Output:** `outputs/` (timestamped).
