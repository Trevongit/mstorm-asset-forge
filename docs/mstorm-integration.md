# MStorm Studio — Integration Guide

This document defines the architectural contract for integrating the **MStorm Asset Forge** with external tools, such as MStorm Studio plugins or automated project pipelines.

## 1. Discovery-First Architectural Pattern

Integration should follow a two-tier discovery pattern to maintain performance and decoupling.

### Tier 1: Discovery via `registry.json`
External tools should first scan `outputs/registry.json`. This file is designed to be a lightweight index of all available assets.

**Safe fields to rely on in the Registry:**
*   `name`: The logical name of the asset.
*   `category`: Primary grouping (e.g., "furniture", "decor").
*   `format`: The exported format (`glb` or `obj`).
*   `dimensions`: Bounding box (WxDxH) in meters for layout planning.
*   `validation_profile`: The quality target used during generation.
*   `material_summary`: High-level material flags (e.g., `emissive`, `metallic`).
*   `package_path`: The relative path to the asset's specific folder.

**Integration Logic:**
Scan the registry to populate an asset browser or to locate specific items by name/tag. Do not scan the filesystem folders directly.

### Tier 2: Detail via `manifest.json`
Once a specific asset is selected for import or deep inspection, read the `manifest.json` located inside the asset's `package_path`.

**Fields found only in the Manifest:**
*   `provenance`: Raw command-line used, LLM metadata, and source type.
*   `geometry_stats`: Detailed vertex and face counts.
*   `validation_results`: Specific warnings or errors encountered.
*   `parametric_options`: Full deterministic inputs used to create the asset.

---

## 2. Recommended Production Path

For **MStorm Studio 2026** integration, the following standards are recommended:

*   **Preferred Format:** `glb` (glTF Binary). It provides the highest fidelity for PBR materials, transparency, and emission.
*   **Handoff Method:** Use the `--sync <target_path>` command to mirror specific registry items into the Studio project's `Assets/` directory.
*   **Decoupling:** External tools should remain agnostic of how the Forge generates geometry. They should only care about the standardized output artifacts defined in the [Package Contract](forge-contract.md).

## 3. Future Bridge Concepts
Future integration improvements may include:
*   **Live Watcher:** A Studio-side plugin that watches `registry.json` for updates.
*   **One-Click Import:** Automatic conversion of Forge registry entries into Studio-native Prefabs.
*   **Metadata Sync:** Propagating Forge tags and dimensions directly into Studio's internal database.
