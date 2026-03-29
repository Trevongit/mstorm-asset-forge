# Future Concept — One-Click Launcher & GUI

This document outlines the conceptual direction for a future graphical interface for the **MStorm Asset Forge**. 

## 1. Vision: The "One-Click" Forge
The Forge is currently a high-fidelity CLI tool. To expand accessibility to non-technical artists and designers, a lightweight local wrapper is envisioned.

### Key Goals:
*   **Visual Discovery:** Transform the `registry.json` into a visual gallery.
*   **Zero-Config Generation:** Provide a "Quick Forge" button for common props.
*   **Live Preview:** Integrated model viewer for both GLB and OBJ exports.

---

## 2. Envisioned UX Modules

### A. The Dashboard (Home)
*   **"Forge of the Day":** A random high-quality preset (e.g., "Dining Table") with a prominent **Forge It!** button.
*   **Recent Activity:** Quick links to the last 5 generated packages.
*   **One-Click Sync:** A "Sync All to Project" button based on a saved target path.

### B. The Asset Browser (Gallery)
*   **Visual Cards:** Each asset shown as a card using its generated `preview.png`.
*   **Metadata Badges:** Visual indicators for polycount (Low/High), format (GLB/OBJ), and validation status (Pass/Warn).
*   **Interactive Filters:** Side-bar for filtering by Category, Material (Metallic/Emissive), or Validation Profile.

### C. The "Demo Mode" (Fun Path)
*   A playful mode for showcasing the forge's speed.
*   **"Auto-Forge" loop:** Randomly generates variations of a preset family and displays them in a carousel.
*   Useful for stress-testing and "infinite" prop brainstorming.

---

## 3. Technical Implementation Strategy
*   **Unchanged Backend:** The GUI will remain a wrapper around `main_forge.py`. It will communicate solely by executing CLI commands or reading the `registry.json`.
*   **Local Web-UI:** Recommended technology is a lightweight FastAPI or Flask server serving a React/Vue frontend, or a standalone Electron unit.
*   **Discovery Engine:** The GUI will rely on the enriched registry implemented in Phase 6 Slice 3.

## 4. Why This Matters
Providing a graphical entry point lowers the barrier to entry, increases the "confidence-building" factor for new users, and provides an immediate way to visualize the forge's outputs without leaving the environment.
