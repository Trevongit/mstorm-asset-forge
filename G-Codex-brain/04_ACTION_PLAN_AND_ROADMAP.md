# 04 ACTION PLAN AND ROADMAP

## Phase 1: Foundation (Completed)
- [x] **Orchestration:** `main_forge.py` CLI with batch and JSON support.
- [x] **Automation:** Headless Blender OBJ/Preview/Stats flow.
- [x] **Agent Skeleton:** Rule-based interpretation and LLM Connector.

## Phase 2: Intelligence & Refinement (Completed)
- [x] **GLB Restoration:** Fixed environment issues to restore glTF support.
- [x] **Parametric:** Added bevel, subdiv, and auto-smooth to contract.
- [x] **Framing:** Implemented adaptive bounding-box camera placement.
- [x] **Sandbox:** Added experimental prompt-to-bpy mode with safety validator.

## Phase 3: Consumer Integration (Completed)
- [x] **Registry:** Persistent logical latest-asset library index (`registry.json`).
- [x] **Packaging:** Added optional ZIP archive support for distributable assets.
- [x] **Library Management:** Added `--prune` utility for historical cleanup.

## Phase 4: Production Handoff & Validation (Completed)
- [x] **Validation:** Post-generation integrity and performance checks.
- [x] **Project Sync:** Helper to copy registry items to external project paths.
- [x] **Integrity:** Hardened success signals and artifact verification.
- [x] **Batch Architect:** LLM-driven multi-item generation from a single prompt.

## Phase 5: Advanced Automation (Next)
- [ ] **Visual Critique:** Automated feedback loop using rendered previews to refine geometry.
- [ ] **Geometry Library:** Pre-baked high-quality BPY templates for common furniture/assets.
- [ ] **Material Support:** Expand contract to support PBR material parameters (Metal/Rough).
