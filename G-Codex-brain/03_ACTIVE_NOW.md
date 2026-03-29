# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. All core Phase 5 features (Modular props, richer materials, library explorer) are committed and verified.

## Feature Matrix

### 1. Stable Production Features (Committed)
* **Deterministic Pipeline:** Structured CLI/JSON requests -> Blender orchestration -> packaged output -> library registry.
* **Multi-Format Export:** GLB/glTF (preferred production path) and OBJ/MTL supported.
* **Artifact Integrity:** Hard-fail mechanism if entry-point artifact is missing or empty.
* **Validation Layer:** Post-generation gates for file size, face count, and package structure.
* **Library Management:** logical latest-asset `registry.json`, utilities: `--list`, `--info`, `--prune`.
* **Project Handoff:** Dedicated `--sync <target>` utility with optional name/category filtering.
* **Packaging:** Optional ZIP archive generation (`--zip`) for distributable units.
* **Better Material Contract:** Support for `base_color`, `metallic`, `roughness`, `emission_color`, `emission_strength`, `alpha`.
* **Modular Props:** Deterministic compound assemblies (`table`, `stool`, `crate`).
* **Visuals:** Adaptive bounding-box aware `preview.png` generation.

### 2. Experimental Features
* **LLM Batch Architect:** Using `--llm-batch` for single-prompt multi-item generation.
* **Prompt-to-BPY Sandbox:** Using `--prompt-to-bpy` for code injection.

## Phase 6 Focus: Scaling & Guidance
1.  **Integration Guidance** (Slice 4 - COMPLETE): Added guides for MStorm integration and quick-start paths.
2.  **Asset Presets Expansion**: Adding more complex recipes (e.g., `shelf_simple`).
3.  **Richer Explorer UX**: Multi-field filtering and material-based search.

## Session Anchor
* **Repo:** `mstorm-asset-forge`
* **Main Entry:** `main_forge.py`
* **Guides:** [Quick Start](../docs/quick-start.md) | [MStorm Integration](../docs/mstorm-integration.md) | [GUI Concept](../docs/future-launcher-concept.md)
* **Explorer Source of Truth:** `outputs/registry.json`
