# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 5: Advanced Deterministic Features (Active).**

## Status Summary
The Forge is a **hardened, production-ready bridge** for local asset generation. It is fully aligned with the `mstorm-asset-forge` identity and provides a clean transition for future agentic development.

## Feature Matrix

### 1. Stable Production Features
- **Deterministic Pipeline:** Structured JSON/CLI requests -> Blender -> Package.
- **Multi-Format:** Full support for **GLB/glTF** and **OBJ/MTL**.
- **Library Management:** logical latest-asset `registry.json`, `--list`, `--info`, and `--prune`.
- **Handoff Tools:** `--sync <target>` utility for external project integration.
- **Integrity & Validation:** Post-generation checks for file existence, size, and polycount.
- **PBR Materials:** base_color (hex/rgb), metallic, and roughness support.
- **Visuals:** Adaptive bounding-box aware `preview.png` generation.

### 2. Experimental Features
- **LLM Batch Architect:** Multi-item generation from a single prompt (`--llm-batch`).
- **Prompt-to-BPY Sandbox:** Safe code injection for custom geometry (`--prompt-to-bpy`).

### 3. Engineering Reference
- **Roadmap:** [docs/engineering-roadmap.md](../docs/engineering-roadmap.md)
- **Continuation:** [docs/development-continuation-guide.md](../docs/development-continuation-guide.md)
- **Contract:** [docs/forge-contract.md](../docs/forge-contract.md)

## Next 3 Tasks
1.  **Modular Assembly:** Support compound props like `table`, `shelf` (Phase 5 Slice 3).
2.  **Rich Explorer:** Add sorting and JSON output to `--list` (Phase 5 Slice 4).
3.  **Advanced Materials:** Implement material presets (Phase 5 Slice 5).

## Session Anchor
- **Repo:** `mstorm-asset-forge` (GitHub Trevongit/mstorm-asset-forge)
- **Active Contract:** MVP v0.1 (Hardened).
- **Baseline Format:** GLB.
