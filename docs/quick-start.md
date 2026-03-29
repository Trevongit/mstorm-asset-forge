# User Quick-Start Guide

Follow this path for immediate success with the **MStorm Asset Forge**.

## 1. First Successful Command
Generate a high-quality GLB sphere with PBR materials.

```bash
python3 main_forge.py --name "first_asset" --primitive "sphere" --format "glb" --color "#00AAFF" --metallic 0.8 --roughness 0.2
```

## 2. Recommended Daily Workflow

### Browse Your Library
List all assets, sorted by date (newest first).
```bash
python3 main_forge.py --list
```

### Inspect Technical Truth
View the full manifest metadata for a specific asset in JSON format.
```bash
python3 main_forge.py --info "first_asset" --json
```

### Handoff to Studio
Sync your validated assets to an external project directory.
```bash
python3 main_forge.py --sync "../MyStudioProject/Assets/"
```

### Library Maintenance
Dry-run cleanup to see what stale packages would be removed.
```bash
python3 main_forge.py --prune --dry-run
```

---

## 3. "Just Want To See It Work?"
If you want to see the forge build a complex assembly immediately:
```bash
python3 main_forge.py --name "demo_chair" --preset "chair_basic" --format "glb" --color "#AA3333"
```
This command exercises the assembly logic, PBR contract, and GLB export in one move.
