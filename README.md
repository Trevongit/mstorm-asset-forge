# MStorm Asset Forge

> **Notice:** This repository is a standalone local asset generation tool for **MStorm Studio 2026**. It is a fork and adaptation of the original LL3M project.

## Overview
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets. It transforms structured requests into standard, packaged asset directories via local Blender orchestration.

## Key Features (Stable)
*   **Production Pipeline:** Structured JSON/CLI -> Blender (Headless) -> Validated Package.
*   **Multi-Format:** Reliable **GLB/glTF** and **OBJ/MTL** export.
*   **Library Explorer:** List, filter, and inspect your assets via `--list` and `--info`.
*   **Handoff Tools:** Project-aware `--sync` and safety-first `--prune` maintenance.
*   **Visuals:** Automated adaptive bounding-box aware previews.

## Engineering Resources
*   **[Engineering Roadmap](docs/engineering-roadmap.md):** Future phases and logical slices.
*   **[Development Continuation Guide](docs/development-continuation-guide.md):** How to pick up and continue development.
*   **[Package Contract](docs/forge-contract.md):** Technical specification for inputs and outputs.

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
    python3 main_forge.py --name "my_table" --primitive "cube" --format "glb" --color "#FFD700" --metallic 1.0
    ```

## Attribution & License
This project is a standalone local fork and adaptation of the **LL3M** project, originally developed by **Threedle at the University of Chicago**.

*   **Project Origin:** [LL3M (GitHub)](https://github.com/threedle/ll3m)
*   **Detailed Attribution:** See [NOTICE.md](NOTICE.md) for origin and attribution details.
*   **Legal Text:** See [LICENSE](LICENSE) for the definitive and controlling license terms (AGPL-3.0).
