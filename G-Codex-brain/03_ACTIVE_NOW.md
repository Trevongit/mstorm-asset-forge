# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 4: Production Handoff & Validation (COMPLETE).**

## Status Summary
The Forge is now a **hardened, project-ready bridge**. It not only generates assets but validates their integrity and provides a project-aware sync mechanism for MStorm Studio handoff.

## Feature Matrix

### 1. Stable Production Features
*   **Integrity Gate**: Mandatory post-Blender verification of entry-point existence and non-zero size.
*   **Asset Validation**: Automatic checks for poly-count thresholds (>50k faces) and file size (>50MB).
*   **Project Sync**: Powerful **`--sync <target_path>`** utility with name and category filtering.
*   **Production Handoff**: Overwrite-always mirror logic for clean external project integration.
*   **Library Indexing**: Persistent `registry.json` and session-wide `run_report.json`.
*   **Multi-Format**: Fully verified OBJ/MTL and GLB/glTF export paths.

### 2. Experimental Features
*   **LLM Batch Architect**: Single prompts can now drive multi-item batch generation (`--llm-batch`).
*   **Prompt-to-BPY Sandbox**: Safe code injection for custom geometry creation.

### 3. Known Limitations
*   **Static Props Only**: Focus remains on non-rigged, non-animated items.
*   **Manual Dependency**: GLB still requires local `numpy` (project-local `.venv` supported).

## Session Anchor
*   **Active Contract**: MVP v0.1 (Hardened).
*   **Main Entry**: `main_forge.py`.
