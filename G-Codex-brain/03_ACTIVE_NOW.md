# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. All core functionality is committed and verified up to Phase 6 Slice 6.

## Feature Matrix

### 1. Stable Production Features (Committed)
*   **Deterministic Pipeline:** CLI/JSON -> Blender orchestration -> Packaged Unit -> Registry.
*   **Multi-Format Export:** **GLB/glTF** (preferred) and OBJ/MTL.
*   **Artifact Integrity:** Hard-fail on missing or empty model artifacts.
*   **Validation Profiles:** `mobile`, `standard`, `high_fidelity` gates.
*   **Library Core:** Enriched `registry.json` discovery layer and detailed `manifest.json`.
*   **Handoff Tools:** `--sync` project mirroring and `--prune` maintenance.
*   **Richer Material Contract:** PBR, Emission, and Alpha support.
*   **Asset Presets:** 10+ deterministic recipes (e.g., `chair_dining`, `pillar_square`).

### 2. Experimental Features
*   **LLM Batch Architect:** Single-prompt multi-item generation.
*   **Prompt-to-BPY Sandbox:** Custom code injection for geometry.

### 3. Known Limitations
*   Static props only; no rigs or characters.
*   No built-in texture authoring pipeline.
*   GUI/Browser is currently a conceptual roadmap item.

---

## How To Get Productive Quickly
1.  **Repo Truth Pass:** run `python3 main_forge.py --list` to see the current library.
2.  **Verify Flow:** run `python3 main_forge.py --name "test" --primitive "cube" --format "glb"`
3.  **Read Contract:** consult `docs/forge-contract.md`.
4.  **Pick a Move:** proceed to `G-Codex-brain/04_ACTION_PLAN_AND_ROADMAP.md`.

## Session Anchor
*   **Repo Identity:** `mstorm-asset-forge`
*   **Preferred Format:** GLB
*   **Key Guides:** [MStorm Integration](../docs/mstorm-integration.md) | [Quick Start](../docs/quick-start.md) | [Agent Guide](../docs/development-continuation-guide.md)
