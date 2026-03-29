# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 1: Deterministic Pipeline & Agent Skeleton (COMPLETE).**

## What Works Right Now
*   **Orchestration:** `main_forge.py` supports CLI, JSON file, and Sequential Batch modes.
*   **Agent Layer:** Rule-based interpretation and LLM Connector architecture (with Mock and OpenAI backends).
*   **Documentation:** Formalized Contract v0.1, NOTICE, and modernized README.
*   **Automation:** Headless Blender (4.0.2) automation for OBJ/MTL export, `preview.png` rendering, and geometry stats extraction.
*   **Reporting:** Automatic `run_report.json` generated for each session.

## What is NOT Implemented / Still Limited
*   **GLB Support:** Currently blocked by system-level library issues (`_ctypes`).
*   **Dynamic Logic:** No prompt-to-bpy generation yet; limited to basic primitives.
*   **Self-Critique:** No automated feedback loop using rendered previews.

## Next Phase: Intelligence & Refinement
1.  **Dynamic Generation:** Implement local LLM prompting to generate custom `bpy` mesh logic (beyond primitives).
2.  **Environment Restoration:** Resolve the `_ctypes` issue to restore glTF/GLB export.
3.  **Autonomous Loop:** Add a "Critique Agent" that inspects `preview.png` and suggests geometry refinements.

## Session Anchor
*   **Active Contract:** MVP v0.1.
*   **Baseline Format:** OBJ/MTL.
*   **Main Entry:** `main_forge.py`.
