# Future Concept — Local Launcher & Demo Viewer

This document outlines the conceptual vision for a graphical user interface (GUI) wrapper for the **MStorm Asset Forge**. 

> **Note:** This GUI does not yet exist. It is a planned developmental arc that builds on the current stable CLI backend.

## 1. Vision: The "Zero-Friction" Forge
The Forge is currently a high-fidelity technical tool. To expand its reach to non-technical designers, a lightweight local GUI is envisioned to surface its capabilities visually.

## 2. Core Modules

### One-Click Generator
*   A Dashboard with prominent buttons for common presets (e.g., "Dining Table", "Crate").
*   Real-time parameter sliders for scale, color, and metallic properties.
*   A playful **"Demo Mode"** that auto-generates variations of an asset family.

### Visual Asset Gallery
*   A visual browser powered by `registry.json`.
*   Asset "cards" displaying the generated `preview.png`.
*   Badges for validation status (OK/WARN), format (GLB/OBJ), and dimensions.

### Integrated Demo Viewer
*   A 3D viewport using a lightweight GLB/OBJ viewer (e.g., Three.js).
*   Allows users to "see it working" immediately after generation.

---

## 3. Staged Implementation Path

1.  **Phase A: Launcher Wrapper**
    *   A simple GUI that maps form inputs to `main_forge.py` CLI commands.
    *   Surfaces the CLI stdout in a scrolled window.

2.  **Phase B: Local Library Browser**
    *   Implements the Gallery view over the current `outputs/` folder.
    *   Provides "Sync to Project" buttons next to each asset card.

3.  **Phase C: Rich Previewer**
    *   Integrates the 3D viewer and "Demo Mode" auto-generator.

## 4. Technical Continuity
The GUI will remain a pure wrapper. All generation, validation, and indexing logic will continue to live in the core Python backend, ensuring the **stabled deterministic contract** is preserved regardless of the interface used.
