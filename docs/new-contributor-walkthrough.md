# New Contributor Walkthrough

This guide is the fastest path from clone to a verified generated asset.

## 1. Preflight (1 minute)

Run these checks from repo root:

```bash
python3 --version
blender --version
```

Expected:
- Python 3.10+ available.
- Blender 4.0+ available in `PATH`.

## 2. Install (2 minutes)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional for prompt/LLM mode:

```bash
cp .env.example .env
# then set OPENAI_API_KEY or GEMINI_API_KEY
```

## 3. First Successful Run (fast, reliable)

Use a deterministic preset and disable preview render for speed:

```bash
python3 main_forge.py \
  --name "hello_chair" \
  --preset "chair_basic" \
  --format "glb" \
  --color "#4A6FA5" \
  --no-preview
```

Why `--no-preview` first: this avoids render-time delays and validates the core generation path.

## 4. Inspect What Was Produced

```bash
python3 main_forge.py --list --view detailed
python3 main_forge.py --info "hello_chair" --json
```

Look at:
- `outputs/registry.json` for discovery/indexing.
- `outputs/<timestamp>_hello_chair/manifest.json` for detailed asset truth.

## 5. Full Packaging Variant (ZIP + validation profile)

```bash
python3 main_forge.py \
  --name "hello_chair_packaged" \
  --preset "chair_basic" \
  --format "glb" \
  --zip \
  --validation-profile standard \
  --no-preview
```

## 6. Daily Contributor Commands

Generate:

```bash
python3 main_forge.py --name "cube01" --primitive "cube" --format "glb" --no-preview
```

List/filter:

```bash
python3 main_forge.py --list --sort date --view detailed
python3 main_forge.py --list --format glb --profile mobile
```

Maintenance:

```bash
python3 main_forge.py --prune --dry-run
python3 main_forge.py --sync "../MyProject/Assets/"
```

## 7. Common Issues

- `Blender executable not found`: install Blender and ensure `blender` is in `PATH`.
- Headless timeout on first run: retry with `--no-preview`.
- Prompt mode fails with API error: verify `.env` keys and provider/model flags.
- Explorer returns empty list: confirm assets were generated into the same `--output-dir`.

## 8. Where To Read Next

- `docs/quick-start.md` for basic usage.
- `docs/forge-contract.md` for the formal input/output contract.
- `docs/mstorm-integration.md` for consumer integration behavior.
- `docs/engineering-roadmap.md` for planned slices.
