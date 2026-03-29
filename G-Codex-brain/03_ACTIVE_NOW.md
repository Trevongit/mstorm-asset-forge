# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. Registry enrichment has improved the discovery layer for downstream MStorm Studio integration.

## Feature Matrix

### 1. Stable Production Features (Committed)
* **Deterministic Pipeline:** Structured CLI/JSON requests -> Blender orchestration -> packaged output -> enriched library registry.
* **Enriched Registry:** Discovery-first `registry.json` including `dimensions`, `validation_profile`, and `material_summary`.
* **Validation Profiles:** Stricter checking via `mobile`, `standard`, and `high_fidelity` targets.
* **Asset Presets:** Deterministic named recipes (e.g., `chair_basic`, `shelf_simple`).
* **Multi-Format Export:** GLB/glTF (preferred production path) and OBJ/MTL supported.
* **Artifact Integrity:** Hard-fail mechanism if entry-point artifact is missing or empty.
* **Library Explorer:** Advanced `--list` features with `--sort`, `--json`, and profile/category filtering.
* **Better Material Contract:** Support for `base_color`, `metallic`, `roughness`, `emission_color`, `emission_strength`, `alpha`.
* **Modular Props:** Deterministic compound assemblies (`table`, `stool`, `crate`).

### 2. Experimental Features
* **LLM Batch Architect:** Using `--llm-batch` for single-prompt multi-item generation.
* **Prompt-to-BPY Sandbox:** Using `--prompt-to-bpy` for code injection.

## Phase 6 Focus: Finalizing Scaling
1.  **Explorer Improvements** (Slice 4): Multi-field filtering and material-based search.
2.  **Asset Presets Expansion**: Refining existing recipes and adding `dining_table_basic` variants.

## Session Anchor
* **Repo:** `mstorm-asset-forge`
* **Main Entry:** `main_forge.py`
* **Discovery Truth:** `outputs/registry.json` (Enriched)
* **Detailed Truth:** `manifest.json` (Per-asset)
