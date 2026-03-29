# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 6: Archetypes & Production Scaling (ACTIVE).**

## Status Summary
The forge is now a **hardened, production-ready deterministic asset pipeline** for local 3D asset generation and packaging. It is intended to be easy for a new engineering agent to continue without rediscovery.

Current system capabilities include:
* Validated asset output with integrity gates.
* Modular prop assembly from deterministic recipes.
* Rich library exploration with sorting and programmatic JSON output.
* Production sync/handoff tooling for external project integration.
* Precise deterministic material control (PBR, Emission, Transparency).
* LLM-assisted batch generation for controlled workflows.

## Stable Production Features (Committed)
The following capabilities are fully implemented and verified in the current `main` branch:

* **Deterministic Pipeline:** Structured CLI/JSON requests -> Blender orchestration -> packaged output -> library registry.
* **Multi-Format Export:** GLB/glTF (preferred production path) and OBJ/MTL supported.
* **Artifact Integrity:** Hard-fail mechanism if entry-point artifact is missing or empty (0 bytes).
* **Validation Layer:** Post-generation gates for file size, face count, and package structure.
* **Library Management:** logical latest-asset `registry.json`, `run_report.json`, and utilities: `--list`, `--info`, `--prune`.
* **Library Explorer:** Advanced `--list` features with `--sort` (name/date) and `--json` output.
* **Project Handoff:** Dedicated `--sync <target>` utility with optional name/category filtering.
* **Packaging:** Optional ZIP archive generation (`--zip`) for distributable units.
* **Better Material Contract:** Support for `base_color`, `metallic`, `roughness`, `emission_color`, `emission_strength`, `alpha`, and `material_name`.
* **Modular Props:** Deterministic compound assemblies including `table`, `stool`, and `crate`.
* **Preview Rendering:** Automatic adaptive bounding-box aware `preview.png` generation.
* **Engineering Identity:** All repository assets and documentation aligned to the `mstorm-asset-forge` identity.

## Experimental Features
The following features are available but considered non-deterministic or future-facing:

* **LLM Batch Architect:** Using `--llm-batch` to generate multi-item requests from a single natural language prompt.
* **Prompt-to-BPY Sandbox:** Using `--prompt-to-bpy` for safe code injection into geometry generation.

## Known Limitations
* **Static Props Only:** No support for rigs, animations, or characters in the current MVP.
* **GLB Priority:** GLB remains the primary production handoff path; OBJ/MTL has limited fidelity for advanced PBR (emission/alpha).
* **Authoring:** No built-in texture authoring or procedural material generation beyond BSDF parameters.
* **Metadata:** Registry is optimized for discovery, but richer semantic metadata (dimensions, vibe) is a Phase 6 goal.

## Phase 6 Focus: Archetypes & Production Scaling
The active development direction focuses on scaling the forge for high-volume production:

1. **Asset Presets / Archetypes**
   * Implementing deterministic named asset recipes (e.g., `chair_basic`, `shelf_simple`).
   * Ensuring repeatable, reusable design intent across project families.

2. **Validation Expansion**
   * Introducing profile-based validation (e.g., `mobile` vs `high_fidelity`).
   * Tighter production readiness checks per-target.

3. **Registry Enrichment**
   * Adding richer discovery metadata (dimensions, material summary, validation profile).
   * Improving library searchability for programmatic consumers.

4. **Future Automation Support**
   * Laying foundations for optional vision-based critique and higher-level agentic planning.

## Session Anchor
* **Repo:** `mstorm-asset-forge`
* **Main Entry:** `main_forge.py`
* **Active Contract:** Hardened deterministic forge contract (`docs/forge-contract.md`)
* **Preferred Handoff Format:** GLB
* **Explorer Source of Truth:** `outputs/registry.json`
