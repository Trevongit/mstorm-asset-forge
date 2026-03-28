# 02 ETHOS AND PRODUCT PRINCIPLES

## Vision
**MStorm Asset Forge** is a local-first bridge for generating and assembling 3D assets for **MStorm Studio 2026**. It transforms abstract requests into structured, MStorm-compatible packages via local Blender orchestration.

## Product Principles (Static Prop Focus)
1.  **Static Prop Priority:** MVP only supports static objects (no rigs, no characters, no animation).
2.  **Local-First:** No reliance on cloud-only black boxes for core generation.
3.  **MStorm Package:** The output is a folder containing a GLB, a manifest, and optional previews.
4.  **Low-Friction:** A single CLI command results in a ready-to-use asset package.
5.  **Clean Export:** Ensure high-fidelity GLB exports from Blender with standard naming conventions.

## One-Day MVP Recommendation
*   **Realistic Scope:** A CLI tool that takes a script/prompt, executes it in Blender, and packages the result into a standardized asset folder.
*   **Key Deliverable:** A valid `asset.glb` and a functional `manifest.json`.

## What it is NOT
*   Not a full 3D suite.
*   Not a character creator or animation engine.
*   Not MStorm Studio itself.
