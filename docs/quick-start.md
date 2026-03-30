# User Quick-Start Guide

Follow this path for immediate success with the **MStorm Asset Forge**.

## 1. First Successful Commands

### Generate a simple asset
```bash
python3 main_forge.py --name "cube01" --primitive "cube" --format "glb"
```

### Generate a complex preset (Happy Path)
```bash
python3 main_forge.py --name "dining_table" --preset "dining_table_basic" --format "glb" --color "#442211"
```

## 2. Browse and Inspect

### List Assets
Shows all generated assets, newest first.
```bash
python3 main_forge.py --list
```

### View Detailed Truth
```bash
python3 main_forge.py --info "dining_table" --json
```

## 3. Sync to Your Project
Handoff your validated assets to an external project directory.
```bash
python3 main_forge.py --sync "../MyProject/Assets/"
```

## 4. Maintenance
Dry-run cleanup to see what stale packages would be removed.
```bash
python3 main_forge.py --prune --dry-run
```

---

## Recommended Daily Workflow
1.  **Generate** using `--format glb` for best quality production handoff.
2.  **Verify** using `--list` to check validation status and dimensions.
3.  **Sync** using `--sync` to mirror into your production environment.

---

## Just Want To See It Work?
If you want to see the forge build a complex assembly immediately:
```bash
python3 main_forge.py --name "demo_chair" --preset "chair_basic" --format "glb" --color "#AA3333"
```
Check the `outputs/` folder for your new production-ready asset.
