# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 5: Advanced Deterministic Features (COMPLETED).**

## Status Summary
The Forge is a **hardened, production-ready bridge** for local asset generation. Phase 5 has significantly improved the visual and organizational capabilities of the forge.

## Feature Matrix

### 1. Stable Production Features (Committed)
- **Deterministic Pipeline:** Structured JSON/CLI requests -> Blender -> Package.
- **Multi-Format:** Full support for **GLB/glTF** (preferred) and **OBJ/MTL**.
- **Library Management:** logical latest-asset `registry.json`, richer `--list` (sorting/json), `--info` (json), and `--prune`.
- **Handoff Tools:** `--sync <target>` utility for external project integration.
- **Integrity & Validation:** Post-generation checks for file existence, size, and polycount.
- **Better Material Contract:** base_color, metallic, roughness, emission, and alpha support.
- **Modular Props:** table, stool, crate assemblies.
- **Visuals:** Adaptive bounding-box aware `preview.png` generation.

### 2. Experimental Features
- **LLM Batch Architect:** Multi-item generation from a single prompt (`--llm-batch`).
- **Prompt-to-BPY Sandbox:** Safe code injection for custom geometry (`--prompt-to-bpy`).

## Next Phase: Phase 6 — Archetypes & Production Scaling
1.  **Asset Presets:** Pre-baked deterministic named asset recipes.
2.  **Validation Expansion:** Profile-based constraints (mobile/desktop).
3.  **Registry Enrichment:** Add dimensions and material vibe to discovery.

## Session Anchor
- **Repo:** `mstorm-asset-forge`
- **Active Contract:** MVP v0.1 (Hardened).
- **Baseline Format:** GLB.
