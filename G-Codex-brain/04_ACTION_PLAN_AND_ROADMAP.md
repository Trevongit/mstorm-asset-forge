# 04 ACTION PLAN AND ROADMAP

## 1) Completed Foundations (Phases 1–5)
The core engine of the MStorm Asset Forge is complete and hardened.

* [x] **Blender Orchestration:** Headless OBJ/GLB generation pipeline.
* [x] **Validated Packaging:** Artifact integrity gates and PBR manifest writing.
* [x] **Library Core:** Enriched `registry.json` discovery layer.
* [x] **Explorer UX:** Sorting, JSON output, and info drill-down.
* [x] **Material Contract:** Alpha, Emission, and PBR property support.
* [x] **Handoff:** Project sync utility and library pruning.

## 2) Phase 6: Archetypes & Production Scaling (Active)

### Slice 7: Guidance & Continuation (COMPLETED)
*   **Goal:** Strengthen the handoff path for humans and agents.
*   **Outcome:** Refined Quick-Start, MStorm Integration, and Agent Guides.

### Slice 8: Rich Explorer Improvements
*   **Goal:** Make the library genuinely usable at scale for daily production.
*   **Candidate Tasks:** Filtering by validation status, material traits, or archetype. Compact vs detailed view modes.

### Slice 9: Asset Presets v3 (Environment Detail)
*   **Goal:** Expand the library of deterministic recipes for environment props.
*   **Examples:** `bookshelf_large`, `crate_slatted`, `pillar_round_base`.

---

## 3) Suggested Next 5 Development Moves
1.  **Enhance Explorer UX:** (Slice 8) Improve searchability for artists.
2.  **Expand Presets:** Add 5 more high-quality deterministic furniture archetypes.
3.  **Refine Sync Tooling:** Support "exclude" patterns for project mirroring.
4.  **Integration Bridge:** (Conceptual) A bridge plugin for MStorm Studio.
5.  **Launcher Wrapper:** (Phase 7) Begin the local-first GUI wrapper concept.

## 4) Rules For Future Contributors And Agents
To maintain the integrity of the forge, all contributors must follow these rules:

1.  **Repo Truth Pass:** Always verify the current committed hashes and tree state before writing code.
2.  **Surgical Slices:** Prefer narrow, verifiable logical slices over broad speculative rewrites.
3.  **Discovery vs Truth:** Keep `registry.json` lean (discovery) and `manifest.json` detailed (per-asset truth).
4.  **No Speculation:** Do not imply that unbuilt GUI or plugin features exist in production-facing docs.
5.  **Deterministic Priority:** Maintain the stability of the deterministic generation path.
6.  **State Distinction:** clearly distinguish between **Committed Reality** and **Planned Future Work**.

---

## How To Continue Development Without Rediscovery
*   **Verify State:** Use `python3 main_forge.py --list` to see the current library.
*   **Read Contract:** Check `docs/forge-contract.md` for the data schema.
*   **Stick to the Roadmap:** Follow the logical slices defined in Phase 6.
