# MStorm Asset Forge — Development Guide

Welcome, engineer. This document defines the rules for continuing the development of the Asset Forge without context loss or technical drift.

## 1. Core Principles

1.  **Contract Stability:** All generation must adhere to the `docs/forge-contract.md`.
2.  **Surgical Slices:** Prefer narrow, verifiable logical slices over broad rewrites.
3.  **Discovery vs Truth:** Keep `registry.json` lean (discovery) and `manifest.json` detailed (per-asset truth).
4.  **Deterministic Priority:** Maintain the stability of the deterministic path as the primary feature.

---

## 2. How To Continue Development Without Rediscovery

Future agentic contributors and humans should follow these operational rules:

### A. Literal Repo Truth Pass
Always verify the current committed hashes and working tree state before writing code. Use `python3 main_forge.py --list` to see what is currently indexed.

### B. State Distinction
Clearly distinguish between:
*   **Committed Reality:** What is in the current HEAD.
*   **Working Tree:** Uncommitted changes.
*   **Conceptual Roadmap:** Planned but unbuilt features.

### C. Documentation Handoff
Update `docs/` whenever a slice changes a contract or adds a capability. Never imply that unbuilt features exist in production documentation.

### D. Registry-First Discovery
Treat `registry.json` as the discovery layer. If you add a new filter to the explorer, ensure the metadata is available in the registry so you don't force an expensive manifest crawl.

---

## 3. Recommended Workflow

1.  **Verify Baseline:** Run `python3 main_forge.py --name "check" --primitive "cube" --format "glb"` to ensure the environment is healthy.
2.  **Check Roadmap:** Proceed to `docs/engineering-roadmap.md` to identify the next active slice.
3.  **Read the Integration Doc:** Understand how the forge fits into the broader MStorm ecosystem via `docs/mstorm-integration.md`.
