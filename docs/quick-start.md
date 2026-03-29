# User Quick-Start Guide

Get up and running with the **MStorm Asset Forge** in less than 2 minutes.

## 1. Generate Your First Asset
The fastest way to see the forge in action is to generate a standard primitive.

**Generate a shiny gold sphere (GLB):**
```bash
python3 main_forge.py --name "gold_orb" --primitive "sphere" --format "glb" --color "#FFD700" --metallic 1.0 --roughness 0.1
```

**Generate a basic chair using a preset:**
```bash
python3 main_forge.py --name "my_chair" --preset "chair_basic" --format "glb"
```

---

## 2. Explore Your Library
Once you've generated some assets, you can browse them directly from the CLI.

**List all assets (latest first):**
```bash
python3 main_forge.py --list
```

**Find only GLB assets:**
```bash
python3 main_forge.py --list --format "glb"
```

**See full technical details for an asset (JSON):**
```bash
python3 main_forge.py --info "gold_orb" --json
```

---

## 3. Sync to Your Project
When you're ready to use your assets in a 3D engine or another folder, use the sync helper.

**Mirror your library to a project folder:**
```bash
python3 main_forge.py --sync "../MyStudioProject/Assets/"
```

---

## 4. Maintenance
Keep your library clean by removing stale packages not referenced in the registry.

**Dry run (see what would be deleted):**
```bash
python3 main_forge.py --prune --dry-run
```

**Execute cleanup:**
```bash
python3 main_forge.py --prune
```

---

## Recommended Handoff Workflow
1.  **Generate** using `--format glb` for best quality.
2.  **Verify** using `--list` to check dimensions and validation status.
3.  **Handoff** using `--sync` to move assets into your production environment.
