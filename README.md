# MStorm Asset Forge

> **Notice:** This repository has been pivoted from the legacy LL3M cloud client to a standalone local asset generation tool for **MStorm Studio 2026**.

## Overview
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets. It transforms structured requests into standard, packaged asset directories via local Blender orchestration.

## Current Capabilities (MVP v0.1)
*   **Standalone Local CLI:** Orchestrate Blender without a cloud server.
*   **Static Prop Pipeline:** Generate primitives (cube, sphere, cylinder, plane) with custom scaling.
*   **OBJ/MTL Baseline:** Reliable export of 3D geometry and materials.
*   **Automated Previews:** Each asset package includes a rendered `preview.png`.
*   **Standardized Manifests:** JSON metadata including asset IDs, tags, and timestamps.
*   **Request File Input:** Support for complex JSON-based generation requests.

## Quick Start
1.  **Requirement:** Blender 4.0+ must be installed and in your `PATH`.
2.  **Install Dependencies:** `pip install -r requirements.txt`
3.  **Basic Generation:**
    ```bash
    python3 main_forge.py --name "my_table" --primitive "cube" --scale "1.5,2.0,0.1"
    ```
4.  **JSON Request:**
    ```bash
    python3 main_forge.py --file examples/request.json
    ```

## Documentation
For full technical specifications on inputs, outputs, and CLI behavior, see the [MStorm Asset Forge — Package Contract (MVP v0.1)](docs/forge-contract.md).

---

## Limitations
*   **Static Props Only:** No characters, rigs, or animations in current MVP.
*   **GLB/glTF:** Currently blocked by system-level library constraints (using OBJ as baseline).
*   **Primitive Generation:** Advanced geometry requires the upcoming Local Agent integration.

---

## Technical History (Legacy LL3M)
*This project was originally the client for LL3M (multi-agent 3D generation). The legacy cloud-client code (auth, polling, cloud-specific utilities) is currently deprecated and will be removed in future cleanup slices.*
