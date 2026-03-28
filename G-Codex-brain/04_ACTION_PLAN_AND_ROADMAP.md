# 04 ACTION PLAN AND ROADMAP

## Phase 1: Static Prop MVP (Completed)
- [x] **Orchestrator:** Create `main_forge.py` as a server-less CLI.
- [x] **Generator:** Implement simple primitive-based script generation.
- [x] **Exporter:** Implement headless OBJ/MTL export flow.
- [x] **Packager:** Implement `manifest.json` and timestamped folder logic.
- [x] **Milestone 1:** Successful "CLI -> Blender Script -> OBJ/MTL -> Manifest -> Asset Package" round trip.

## Phase 2: Refined Generation (In Progress)
- [ ] **Local Agent:** Implement local LLM caller for dynamic `bpy` code.
- [ ] **Previews:** Add a Blender render pass for `preview.png`.
- [ ] **Metadata:** Expand manifest with tags, provenance, and scale notes.

## Phase 3: MStorm Integration
- [ ] Automated asset indexing for MStorm Studio 2026.
- [ ] GLB restoration (if library issues are resolved).
