# MStorm Asset Forge

> **Notice:** This repository is a hardened, standalone local asset generation tool for **MStorm Studio 2026**.

## Overview
The **MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets. It transforms deterministic requests (CLI/JSON) into standard, validated, and packaged asset directories via local Blender orchestration.

*   **Deterministic:** Same inputs always yield the same structural geometry.
*   **Production-Ready:** Every asset is validated for integrity and performance thresholds.
*   **Library-First:** Generates an enriched, searchable library index (`registry.json`).
*   **GLB Preferred:** Optimized for glTF/GLB production handoff with full PBR support.

## Fast Demo
Generate a red dining chair (GLB) and check its metadata in one move:
```bash
python3 main_forge.py --name "demo_chair" --preset "chair_dining" --format "glb" --color "#AA3333" --no-preview
python3 main_forge.py --info "demo_chair"
```

## How MStorm Uses This Forge
The Forge is designed to be consumed by external tools (like MStorm Studio) via a discovery-first pattern:

1.  **Discovery Layer (`registry.json`):** Scan this file to browse the library, check dimensions, and resolve asset paths.
2.  **Truth Layer (`manifest.json`):** Read the per-asset manifest for deep technical details, provenance, and validation results.
3.  **Asset Handoff (`entry_point`):** Use the path provided in the registry to import the actual GLB or OBJ file.
4.  **Project Bridge (`--sync`):** Use the built-in sync utility to mirror the Forge library into a specific Studio project folder.

## Current Capabilities
*   **Modular Props:** Deterministic assemblies like `table`, `chair`, `stool`, `shelf`, and `pillar`.
*   **Asset Presets:** Named recipes (e.g., `chair_basic`, `cabinet_basic`) for repeatable generation.
*   **Library Explorer:** CLI tools to list, filter (by trait/profile/status), and sort assets.
*   **Richer Materials:** Full control over `base_color`, `metallic`, `roughness`, `emission`, and `alpha`.
*   **Validation & Integrity:** Profile-based gates (`mobile`, `standard`) and hard-fail integrity checks.
*   **Maintenance:** Automated ZIP packaging, library pruning, and project syncing.

## Quick Start
1.  **Requirement:** Blender 4.0+ in your `PATH`.
2.  **Install:** `pip install -r requirements.txt`
3.  **Generate:** `python3 main_forge.py --name "cube01" --primitive "cube"`
4.  **Explore:** `python3 main_forge.py --list --view detailed`

## Engineering Resources
*   **[Quick-Start Guide](docs/quick-start.md):** The fastest success path for new users.
*   **[MStorm Integration](docs/mstorm-integration.md):** Detailed contract for Studio and external tool integration.
*   **[Package Contract](docs/forge-contract.md):** Technical specification for inputs and outputs.
*   **[Engineering Roadmap](docs/engineering-roadmap.md):** Planned phases and development slices.
*   **[Development Guide](docs/development-continuation-guide.md):** Essential rules for engineers and agents.

## Attribution & License
Standalone local fork and adaptation of the **LL3M** project (University of Chicago).
*   **Legal:** See [LICENSE](LICENSE) (AGPL-3.0).
*   **Origin:** See [NOTICE.md](NOTICE.md).
