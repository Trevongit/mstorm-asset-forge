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
3.  **Local Secrets:** Copy `.env.example` to `.env`, fill in your API keys, and load them into your shell:
    ```bash
    cp .env.example .env
    # Load variables (Linux/macOS)
    set -a; source .env; set +a
    ```
4.  **Basic Generation:**
    ```bash
    python3 main_forge.py --name "my_table" --primitive "cube" --scale "1.5,2.0,0.1"
    ```
4.  **JSON Request:**
    ```bash
    python3 main_forge.py --file examples/request.json
    ```

## Documentation
For full technical specifications on inputs, outputs, and CLI behavior, see the [MStorm Asset Forge — Package Contract (MVP v0.1)](docs/forge-contract.md).

## GLB Export Support
Reliable GLB/glTF export is now supported. 
*   **Note:** If GLB export fails due to missing dependencies (like `numpy`), the system will automatically attempt to use a project-local `.venv` if present. 
*   To ensure compatibility, you can create a local environment: `python3 -m venv .venv && source .venv/bin/activate && pip install numpy`

## Attribution & License
This project is a standalone local fork and adaptation of the **LL3M** project, originally developed by **Threedle at the University of Chicago**.

*   **Project Origin:** [LL3M (GitHub)](https://github.com/threedle/ll3m)
*   **Detailed Attribution:** See [NOTICE.md](NOTICE.md) for origin, attribution, and licensing summaries.
*   **Legal Text:** See [LICENSE](LICENSE) for the definitive and controlling license terms.

---

## Limitations
*   **Static Props Only:** No characters, rigs, or animations in current MVP.
*   **GLB/glTF:** Currently blocked by system-level library constraints (using OBJ as baseline).
*   **Primitive Generation:** Advanced geometry requires the upcoming Local Agent integration.

---

## Technical History (Legacy LL3M)
*This project was originally the client for LL3M. The legacy cloud-client code is currently archived or removed to focus on standalone local orchestration.*
