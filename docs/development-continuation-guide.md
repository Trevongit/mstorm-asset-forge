# MStorm Asset Forge — Development Continuation Guide

Welcome, engineering agent. This project is a standalone local auxiliary tool for **MStorm Studio 2026**. Your mission is to maintain the deterministic integrity of the forge while carefully expanding its intelligence.

## 1. Project Context
- **Identity:** MStorm Asset Forge (local-first asset bridge).
- **Core Stack:** Python 3.12, Blender 4.0.2 (Headless), GLB/OBJ export.
- **Workflow:** Request -> Local LLM/Rules -> Deterministic Contract -> Blender -> Package.

## 2. Engineering Standards
- **Contract First:** All generation must adhere to the schema in `docs/forge-contract.md`. 
- **Safety First:** The experimental BPY sandbox (`--prompt-to-bpy`) uses strict validation in `forge/safety.py`. Never bypass this.
- **Surgical Commits:** Work in narrow logical slices. See `docs/engineering-roadmap.md` for the planned sequence.
- **Verification:** Every slice must include a verification command and a literal repo status report.

## 3. How to Resume Development
1.  **Read the Brain:** Start with `G-Codex-brain/03_ACTIVE_NOW.md` to see the current tactical status.
2.  **Review History:** Check `G-Codex-brain/MERGE_LOG.md` to understand the logical progression of slices.
3.  **Validate Environment:** Run a standard generation test to ensure Blender and Python are correctly configured:
    ```bash
    python3 main_forge.py --name "env_check" --primitive "cube" --format "glb"
    ```
4.  **Pick a Slice:** Select the next slice from the Roadmap and perform a planning pass.

## 4. Key Repository Areas
- `main_forge.py`: CLI entry point and orchestration.
- `forge/generator.py`: Blender Python (`bpy`) script templates.
- `forge/packager.py`: Packaging, Manifest, and Registry logic.
- `forge/llm_connector.py`: OpenAI/Gemini REST API integrations.
- `forge/validator.py`: Post-generation integrity and performance checks.

## 5. Decision Log (Major Patterns)
- **Latest-Only Registry:** `registry.json` tracks only the newest version of a logical asset (name|category|format).
- **Non-Fatal Previews:** Assets succeed even if `preview.png` fails (logged as warning).
- **Hard-Fail Integrity:** Assets fail if the model file is missing or 0 bytes.

## 6. Communication Style
- Be concise and direct.
- Report literal git truth.
- Distinguish clearly between **Stable** and **Experimental** features.
- Provide verification commands for every change.
