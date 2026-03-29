# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. It is designed for seamless continuation by new engineering agents.

Current system capabilities include:
* Validated asset output with multi-profile thresholds.
* Modular prop assembly from deterministic recipes (presets).
* Enriched library discovery via a lightweight registry.
* Production sync/handoff tooling for external project integration.

## Feature Matrix

### 1. Stable Production Features (Committed)
*   **Deterministic Pipeline:** CLI/JSON -> Blender orchestration -> Packaged Unit -> Registry.
*   **Multi-Format Export:** **GLB/glTF** (preferred production path) and OBJ/MTL.
*   **Artifact Integrity:** Automatic hard-fail if model is missing or 0 bytes.
*   **Validation Profiles:** Target-specific gates (`mobile`, `standard`, `high_fidelity`).
*   **Enriched Registry:** Discovery-first `registry.json` including dimensions, PBR summary, and presets.
*   **Library Explorer:** Advanced `--list` features with sorting and JSON output.
*   **Better Material Contract:** Support for `base_color`, `metallic`, `roughness`, `emission_color`, `emission_strength`, `alpha`.
*   **Modular Props & Presets:** Deterministic compound assemblies (e.g., `chair_basic`, `dining_table_basic`).

### 2. Experimental Features
*   **LLM Batch Architect:** Using `--llm-batch` for single-prompt multi-item generation.
*   **Prompt-to-BPY Sandbox:** Using `--prompt-to-bpy` for custom code injection.

### 3. Known Limitations
*   **Static Props Only:** No rigs, animations, or characters.
*   **Authoring:** No built-in texture authoring pipeline yet.
*   **GUI:** Backend is CLI-only; visual wrapper is a planned future phase.

---

## How To Get Productive Quickly
1.  **Repo Truth Pass:** run `git log -n 1` and `git status` to verify the baseline.
2.  **Verify Environment:** run `python3 main_forge.py --name "check" --primitive "cube"` to ensure Blender is responsive.
3.  **Read the Integration Doc:** see `docs/mstorm-integration.md` to understand the data flow.
4.  **Pick a Roadmap Slice:** proceed to `G-Codex-brain/04_ACTION_PLAN_AND_ROADMAP.md`.

## Session Anchor
*   **Repo Identity:** `mstorm-asset-forge`
*   **Primary Logic:** `main_forge.py`
*   **Preferred Format:** GLB
*   **Discovery Truth:** `outputs/registry.json`
