# 04 ACTION PLAN AND ROADMAP

## 1) Phase 1–5 Completed Foundations
The core engine of the MStorm Asset Forge is complete and hardened.

* [x] Blender headless generation pipeline
* [x] Preview rendering
* [x] Package manifest and run reporting
* [x] LLM connector base and Gemini/OpenAI support
* [x] GLB restoration
* [x] Adaptive framing
* [x] Sandbox prompt-to-bpy path
* [x] Registry and latest-asset logic
* [x] ZIP packaging
* [x] Prune utility
* [x] Validation layer
* [x] Sync helper
* [x] Artifact-integrity gate
* [x] LLM batch architect
* [x] Modular prop assembly (table, stool, crate)
* [x] Richer library explorer (sorting, JSON)
* [x] Better material contract (emission, alpha, mat_name)

## 2) Phase 6: Archetypes & Production Scaling (Active)

### Slice 1 — Asset Presets / Archetypes
* **Goal:** Introduce deterministic named asset recipes and reusable asset families.
* **Examples:** `chair_basic`, `dining_table_basic`, `crate_stackable`, `stool_round`, `shelf_simple`.
* **Requirements:**
    * Keep deterministic behavior (reproducible from same params).
    * Preserve manifest/registry integrity.
    * Support clear preset naming in CLI/JSON.
    * Make presets composable with the material contract.
* **Definition of Done:**
    * At least 3–5 preset/archetype assets implemented in `generator.py`.
    * Documented contract behavior for calling presets.
    * Verified generation and manifest output for all types.

### Slice 2 — Validation Expansion
* **Goal:** Move from generic validation to profile-based validation.
* **Profiles:** `mobile`, `standard`, `high_fidelity`.
* **Checks:** Max file size, max face count, preferred format per profile.
* **Definition of Done:**
    * Validation profiles available via CLI / request options.
    * Manifest captures the chosen validation profile.
    * Meaningful warnings/errors shown in run report based on profile rules.

### Slice 3 — Registry Enrichment
* **Goal:** Improve asset discoverability and future automation.
* **Candidate Fields:** Dimensions (bounding box), validation profile, material summary, preset name.
* **Definition of Done:**
    * Registry remains lean enough for fast discovery.
    * Richer fields added deliberately to the indexing logic.
    * Explorer commands (`--list`, `--info`) benefit from new metadata.

### Slice 4 — Explorer Improvements
* **Goal:** Make the library genuinely usable at scale for daily production.
* **Candidate Improvements:** Filtering by validation status, material properties, or archetype. Compact vs detailed view modes.
* **Definition of Done:** Explorer commands allow efficient management without manual manifest inspection.

## 3) Phase 7 Candidates / Future Expansion
* Texture/material preset packs.
* Studio-target export helpers (MStorm specific packaging).
* Vision-based critique loop (experimental feedback).
* Guided repair/refinement agents.
* Downstream importer validation.

## 4) Continuation Rules for New Agents
Future agentic contributors should follow these principles:

1. **Literal Repo Truth Pass:** Always verify the current committed state and hashes before writing code.
2. **State Distinction:** Clearly distinguish between **Committed** state, **Working Tree** state, **Verified** behavior, and **Intended** roadmap.
3. **Surgical Slices:** Prefer narrow, verifiable logical slices over broad speculative rewrites.
4. **Docs Alignment:** Update `G-Codex-brain` and `docs/` whenever a slice changes the development surface.
5. **Deterministic Core:** Preserve deterministic paths unless a feature is explicitly marked experimental.
6. **Registry vs Manifest:** Treat `registry.json` as the discovery layer and per-asset `manifest.json` as the detailed truth layer.
7. **Append History:** When reconciling history in `MERGE_LOG.md`, do not erase earlier milestones; append and clarify.
8. **No Discovery Memory:** Make continuation easy for the next agent without requiring conversational memory.
