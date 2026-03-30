# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. All core functionality is verified and synchronized with the GitHub remote.

## Feature Matrix

### 1. Stable Production Features (Committed)
*   **Deterministic Pipeline:** CLI/JSON -> Blender orchestration -> Packaged Unit -> Registry.
*   **Multi-Format Export:** **GLB/glTF** (preferred) and OBJ/MTL.
*   **Artifact Integrity:** Automatic hard-fail if model is missing or 0 bytes.
*   **Validation Profiles:** Target-specific gates (`mobile`, `standard`, `high_fidelity`).
*   **Enriched Registry:** Discovery-first `registry.json` including dimensions, PBR summary, and presets.
*   **Library Explorer:** Advanced `--list` features with sorting and JSON output.
*   **Better Material Contract:** Support for `base_color`, `metallic`, `roughness`, `emission_color`, `emission_strength`, `alpha`.
*   **Modular Props & Presets:** Deterministic compound assemblies (e.g., `chair_dining`, `pillar_square`).
*   **Project Handoff:** Dedicated `--sync` utility for project mirroring.

### 2. Experimental Features
*   **LLM Batch Architect:** Using `--llm-batch` for single-prompt multi-item generation.
*   **Prompt-to-BPY Sandbox:** Using `--prompt-to-bpy` for custom code injection.

### 3. Known Limitations
*   Static props only; no rigs, animation, or characters.
*   No built-in texture authoring pipeline yet.
*   Registry is optimized for discovery; deep technical truth remains in manifests.

---

## How To Get Productive Quickly
1.  **Repo Truth Pass:** run `python3 main_forge.py --list` to see the current library.
2.  **Verify Flow:** run `python3 main_forge.py --name "test" --primitive "cube" --format "glb"`.
3.  **Read the Key Docs:**
    *   [MStorm Integration](../docs/mstorm-integration.md)
    *   [Development Guide](../docs/development-continuation-guide.md)
4.  **Pick a Move:** proceed to `G-Codex-brain/04_ACTION_PLAN_AND_ROADMAP.md`.

## Session Anchor
*   **Repo Identity:** `mstorm-asset-forge`
*   **Preferred Format:** GLB
*   **Discovery Truth:** `outputs/registry.json`
