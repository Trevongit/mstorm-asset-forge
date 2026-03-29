# MStorm Asset Forge

> **Notice:** This repository is a hardened, standalone local asset generation tool for **MStorm Studio 2026**.

## Overview
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets. It transforms deterministic requests (CLI/JSON) into standard, validated, and packaged asset directories via local Blender orchestration.

## Fastest Way To See It Work
1.  **Requirement:** Blender 4.0+ in your `PATH`.
2.  **Install:** `pip install -r requirements.txt`
3.  **Generate a gold sphere (GLB):**
    ```bash
    python3 main_forge.py --name "gold_orb" --primitive "sphere" --format "glb" --color "#FFD700" --metallic 1.0
    ```
4.  **Verify in library:**
    ```bash
    python3 main_forge.py --list
    ```

## Engineering Resources
*   **[Quick-Start Guide](docs/quick-start.md):** The minimal success path for new users.
*   **[MStorm Integration](docs/mstorm-integration.md):** How MStorm should consume the forge.
*   **[Package Contract](docs/forge-contract.md):** Technical specification for inputs and outputs.
*   **[Engineering Roadmap](docs/engineering-roadmap.md):** Planned phases and development slices.
*   **[Development Guide](docs/development-continuation-guide.md):** Continuation rules for agents and contributors.
*   **[Future Concept: GUI](docs/future-launcher-concept.md):** Vision for a one-click launcher and viewer.

## Attribution & License
Standalone local fork and adaptation of the **LL3M** project (University of Chicago).
*   **Legal:** See [LICENSE](LICENSE) (AGPL-3.0).
*   **Origin:** See [NOTICE.md](NOTICE.md).
