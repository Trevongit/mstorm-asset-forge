# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 4: Production Handoff & Validation (COMPLETE).**

## Status Summary
The Forge is now a **hardened, production-usable local asset library pipeline**. It not only generates and packages assets but also validates their integrity and provides a project-aware sync mechanism for MStorm Studio handoff.

## Feature Matrix

### 1. Stable Production Features
*   **Artifact Integrity**: Mandatory post-Blender verification of entry-point existence and non-zero size.
*   **Asset Validation**: Automatic checks for poly-count thresholds (>50k faces) and file size (>50MB).
*   **Library Indexing**: Persistent logical latest-asset `registry.json` and session-wide `run_report.json`.
*   **Project Sync**: Powerful **`--sync <target_path>`** utility with name and category filtering.
*   **ZIP Packaging**: Optional single-file distributable archives (`--zip`).
*   **Maintenance**: Safety-first **`--prune`** utility to manage stale historical packages.
*   **Multi-Format**: Fully verified OBJ/MTL and GLB/glTF export paths.
*   **Visuals**: Adaptive, bounding-box-aware `preview.png` for every asset.

### 2. Experimental Features
*   **LLM Batch Architect**: Single prompts can now drive multi-item batch generation (`--llm-batch`).
*   **Prompt-to-BPY Sandbox**: Safe code injection for custom geometry creation (`--prompt-to-bpy`).

### 3. Known Limitations
*   **Static Props Only**: Focus remains on non-rigged, non-animated items.
*   **Manual Dependency**: GLB requires local `numpy` (project-local `.venv` supported).

## Session Anchor
*   **Active Contract**: MVP v0.1 (Hardened).
*   **Baseline Formats**: GLB, OBJ.
*   **Main Entry**: `main_forge.py`.
