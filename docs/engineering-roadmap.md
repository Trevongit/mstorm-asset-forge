# MStorm Asset Forge — Engineering Roadmap

This document outlines the planned development phases for the MStorm Asset Forge. Each phase is broken down into commit-sized slices to ensure stable, verifiable progress.

## Phase 5: Advanced Deterministic Features & Polish (Current)

The goal of Phase 5 is to expand the deterministic core while improving library usability.

### Slice 3: Modular Prop Assembly
- **Goal:** Move beyond simple primitives into deterministic compound props.
- **Scope:** Support prop types like `table`, `stool`, `crate`, `shelf`, `pillar_variant`.
- **Implementation:**
    - Update `forge/generator.py` with modular assembly logic (combining multiple primitives).
    - Expand the contract to include these new prop types.
- **Verification:** Generate a `table` with custom scale and verify all 5 components (top + 4 legs) exist in the exported mesh.

### Slice 4: Better Library Exploration
- **Goal:** Improve the `--list` and `--info` UX.
- **Scope:** 
    - Add sorting (by date, name).
    - Add JSON output format for programmatic consumption.
    - Show validation status in the list view.
- **Verification:** `python3 main_forge.py --list --format json --sort date`.

### Slice 5: Better Material Contract
- **Goal:** Extend the PBR contract beyond basic colors.
- **Scope:** 
    - Add `metallic_map`, `roughness_map` placeholders (future texture support).
    - Implement material "presets" (e.g., `metal_gold`, `wood_rough`, `plastic_shiny`).
    - Document GLB-first material expectations and OBJ limitations.
- **Verification:** Request `material_preset: "metal_gold"` and verify PBR values in manifest.

---

## Phase 6: Archetypes & Production Scaling

Phase 6 focuses on scaling the forge for high-volume production and project-specific needs.

### Slice 1: Asset Presets / Archetypes
- **Goal:** Define deterministic named asset recipes.
- **Description:** Presets are pre-validated JSON requests stored in the repo.
- **Differentiation:** Unlike freeform LLM prompts, presets are guaranteed to be "perfect" and reusable.

### Slice 2: Validation Expansion
- **Goal:** Add stronger mesh and export validation.
- **Scope:** 
    - Check for degenerate geometry (zero-area faces).
    - Implement "Project Profiles" (e.g., `mobile` restricts polycount to 5k, `desktop` to 50k).
- **Verification:** Run validation against a `mobile` profile and verify failure for high-poly spheres.

### Slice 3: Registry Enrichment
- **Goal:** Enhance `registry.json` for better discovery.
- **Scope:** 
    - Include bounding box dimensions in the registry.
    - Include primary material category.
- **Rationale:** Allow consumers to search by "size" or "vibe" without opening individual manifests.

### Slice 4+: Project Profiles & Hybrid Workflow
- **Project Profiles:** Full support for per-project configuration (target format, scale units, max polycount).
- **Hybrid Workflow:** Refine the interaction between deterministic presets and LLM-driven "tweaks".
- **Visual Critique Loop (Experimental):** Automated feedback where a Vision LLM inspects `preview.png` and suggests geometry or material adjustments.

---

## Technical Debt & Maintenance
- **Environment:** Ongoing monitoring of Blender/Python compatibility.
- **Portability:** Ensure CLI remains functional across Linux, Windows, and macOS.
- **Security:** Maintain strict safety rules for the experimental BPY sandbox.
