# 03 ACTIVE NOW

## Purpose
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**.

## Current Phase
**MVP Phase 3: Consumer Integration & Library Management (COMPLETE).**

## Status Summary
The Forge is now a **production-usable local asset library pipeline**. It reliably generates, packages, and indexes assets for downstream consumption by MStorm Studio or other glTF/OBJ loaders.

## Feature Matrix

### 1. Stable Production Features
*   **Multi-Format Export**: Reliable **OBJ/MTL** and **GLB/glTF** support.
*   **Library Indexing**: Persistent `outputs/registry.json` tracking the latest version of every asset.
*   **Distribution**: Optional **ZIP packaging** (`--zip`) for single-file distributable assets.
*   **Maintenance**: Safety-first **`--prune`** utility to manage stale historical folders and archives.
*   **Rich Metadata**: Manifests with vertex/face stats, provenance, unit scale, and author.
*   **Visuals**: Adaptive, bounding-box-aware `preview.png` for every asset.

### 2. Experimental Features
*   **Prompt-to-BPY Sandbox**: Opt-in (`--prompt-to-bpy`) LLM-generated geometry logic with strict safety validation.

### 3. Known Limitations
*   **Static Props Only**: No characters, rigs, or animations yet.
*   **Environment**: Requires `numpy` in the Blender Python path for GLB support (local `.venv` supported).

## Session Anchor
*   **Active Contract**: MVP v0.1 (Stable).
*   **Baseline Formats**: GLB, OBJ.
*   **Main Entry**: `main_forge.py`.
