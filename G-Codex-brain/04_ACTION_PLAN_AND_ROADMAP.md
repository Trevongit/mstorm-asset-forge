# 04 ACTION PLAN AND ROADMAP

## Phase 1: Static Prop MVP (Completed)
- [x] **Orchestrator:** Create `main_forge.py` as a server-less CLI.
- [x] **Exporter:** Implement headless OBJ/MTL export and preview rendering.
- [x] **Packager:** Implement `manifest.json` and timestamped folder logic.
- [x] **Input:** Support `--file` JSON requests and CLI overrides.
- [x] **Formalize:** Document Input/Output contract in `docs/forge-contract.md`.
- [x] **Milestone 1:** Successful "CLI -> Blender -> Package -> Contract" round trip.

## Phase 2: Refined Generation (Next)
- [ ] **Local Agent:** Implement local LLM caller for dynamic `bpy` code.
- [ ] **Complex Props:** Support for modular prop assembly (beyond simple primitives).
- [ ] **Legacy Cleanup:** Remove deprecated LL3M auth and cloud client code.

## Phase 3: MStorm Integration
- [ ] Automated asset indexing for MStorm Studio 2026.
- [ ] GLB restoration (if library issues are resolved).
