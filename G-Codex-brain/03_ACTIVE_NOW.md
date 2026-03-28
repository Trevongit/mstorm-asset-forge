# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**One-Day MVP: Formalization & Documentation (Slice 4).**

## What Works Right Now
*   **Orchestrator:** `main_forge.py` CLI supports flags and JSON file input.
*   **Contract:** Input/Output contract version **MVP v0.1** is formalized and documented.
*   **Blender (4.0.2):** Headless automation for OBJ/MTL export and `preview.png` rendering.
*   **Packaging:** Consistent timestamped asset folders with JSON manifests.

## What is NOT Implemented
*   **Local Agent Strategy:** Dynamic `bpy` generation via LLM.
*   **GLB Support:** Currently blocked by system-level library issues (`_ctypes`).

## Next 3 Tasks
1.  **Local Agent Integration:** Implement a local LLM or template caller for complex geometry.
2.  **Asset Logic Expansion:** Support more complex non-primitive props (e.g., modular furniture).
3.  **Legacy Cleanup:** Begin pruning the deprecated LL3M cloud/auth code.

## Session Anchor
*   **Baseline Format:** OBJ/MTL.
*   **Contract Version:** MVP v0.1 (see `docs/forge-contract.md`).
*   **Main Entry:** `main_forge.py`.
