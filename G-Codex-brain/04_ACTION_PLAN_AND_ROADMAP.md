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
- [x] **Entry Points:** Standardized `entry_point` in manifest for consumers.

## Phase 4: Production Handoff (Next)
- [ ] **Asset Validation:** Add a tool to verify GLB/OBJ files against MStorm constraints.
- [ ] **Batch Generator:** Allow the LLM to generate complex multi-item batch request files.
- [ ] **Studio Bridge:** Export helper to copy assets directly into an MStorm project path.
