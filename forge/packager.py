import json
import os
import datetime
import uuid
import zipfile
import time
import shutil

def prepare_package_dir(output_root, asset_name):
    """
    Creates a standardized package directory.
    """
    timestamp_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"{timestamp_folder}_{asset_name}"
    package_path = os.path.join(output_root, package_name)
    os.makedirs(package_path, exist_ok=True)
    return package_path

def write_manifest(package_path, asset_name, primitive, scale, 
                   tags=None, preview_file=None, author="MStorm Forge", 
                   creation_command=None, geometry_stats=None, 
                   parametric_options=None, source_type="primitive",
                   experimental_mode=False, llm_metadata=None, 
                   entry_point=None, format="obj", archive_file=None, 
                   validation_results=None, version="1.0.0",
                   preset_name=None):
    """
    Writes a manifest.json file to the package directory.
    """
    manifest_timestamp = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    asset_id = str(uuid.uuid4())
    
    final_tags = ["generated", "mvp", "prop", (preset_name or primitive).lower()]
    if experimental_mode:
        final_tags.append("experimental")
    if preset_name:
        final_tags.append("preset")

    if tags:
        for t in tags:
            t_clean = t.strip().lower()
            if t_clean and t_clean not in final_tags:
                final_tags.append(t_clean)
    
    provenance = {
        "source_type": source_type if not preset_name else "preset",
        "creation_command": creation_command or "Manual",
        "experimental_mode": experimental_mode
    }
    if preset_name:
        provenance["preset_name"] = preset_name
    if llm_metadata:
        provenance.update(llm_metadata)

    manifest = {
        "asset_id": asset_id,
        "name": asset_name,
        "type": "static_prop",
        "format": format,
        "entry_point": entry_point,
        "version": version,
        "author": author,
        "generator": "MStorm Asset Forge v0.1",
        "timestamp": manifest_timestamp,
        "provenance": provenance,
        "metadata": {
            "primitive": primitive if not preset_name else "preset_assembly",
            "scale": scale,
            "unit_system": "metric",
            "unit_scale": "1.0 unit = 1.0 meter",
            "is_rigged": False
        },
        "tags": final_tags
    }
    
    if archive_file:
        manifest["archive_file"] = archive_file
    if parametric_options:
        manifest["metadata"]["parametric_options"] = parametric_options
    if preview_file:
        manifest["preview_image"] = preview_file
    if geometry_stats:
        manifest["geometry_stats"] = geometry_stats
    if validation_results:
        manifest["validation_results"] = validation_results
        
    manifest_path = os.path.join(package_path, "manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return manifest_path, asset_id, manifest_timestamp

def create_zip_archive(package_path):
    """
    Creates a zip archive of the package folder.
    """
    package_path = os.path.abspath(package_path)
    parent_dir = os.path.dirname(package_path)
    package_name = os.path.basename(package_path)
    zip_filename = f"{package_name}.zip"
    zip_path = os.path.join(parent_dir, zip_filename)
    
    time.sleep(0.5)
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, package_path)
                    zipf.write(file_path, arcname)
        return zip_filename
    except Exception as e:
        print(f"Forge: WARNING - Could not create zip archive: {e}")
        return None

def write_run_report(output_dir, run_metadata, asset_results):
    """
    Writes a summary run_report.json to the output directory.
    """
    report = {
        "run_metadata": run_metadata,
        "assets": asset_results
    }
    
    report_path = os.path.join(output_dir, "run_report.json")
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        return report_path
    except Exception as e:
        print(f"Forge: WARNING - Could not write run report to {report_path}: {e}")
        return None

def update_global_registry(output_root, asset_info):
    """
    Upserts an asset entry into the global registry.json using a logical key.
    """
    registry_path = os.path.join(output_root, "registry.json")
    registry = {"last_updated": None, "assets": []}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except Exception as e:
            print(f"Forge: WARNING - Could not read registry, starting fresh: {e}")

    def get_logical_key(a):
        cat = a.get('category')
        if cat is None: cat = ""
        return f"{a.get('name')}|{cat}|{a.get('format')}"

    new_key = get_logical_key(asset_info)
    assets = registry.get("assets", [])
    
    updated_assets = []
    found = False
    for a in assets:
        if get_logical_key(a) == new_key:
            updated_assets.append(asset_info)
            found = True
        else:
            updated_assets.append(a)
            
    if not found:
        updated_assets.append(asset_info)
        
    registry["assets"] = updated_assets
    registry["last_updated"] = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    
    try:
        os.makedirs(output_root, exist_ok=True)
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=4)
        return registry_path
    except Exception as e:
        print(f"Forge: WARNING - Could not update global registry: {e}")
        return None

def prune_stale_assets(output_root, dry_run=False):
    """
    Safely removes stale asset folders and zip archives.
    """
    registry_path = os.path.join(output_root, "registry.json")
    if not os.path.exists(registry_path):
        raise FileNotFoundError(f"Registry not found at {registry_path}. Pruning requires a valid registry.")

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Could not read registry: {e}")

    referenced_items = set()
    for a in registry.get("assets", []):
        for field in ["package_path", "archive_path", "entry_point", "preview_path"]:
            val = a.get(field)
            if val:
                top_level = val.split(os.sep)[0]
                referenced_items.add(top_level)

    all_on_disk = os.listdir(output_root)
    to_remove = []
    protected = []
    
    permanent = ["registry.json", "run_report.json"]

    for item in all_on_disk:
        if item.startswith(".") or item in permanent or item in referenced_items:
            protected.append(item)
            continue
            
        item_path = os.path.join(output_root, item)
        if os.path.isdir(item_path) or item.endswith(".zip"):
            to_remove.append(item)
        else:
            protected.append(item)

    if dry_run:
        print("\n--- PRUNE DRY RUN ---")
        print("Protected items (preserved):")
        for item in sorted(protected):
            print(f" [KEEP] {item}")
        print("\nStale items (marked for removal):")
        for item in sorted(to_remove):
            print(f" [REMOVE] {item}")
    
    removed_folders = 0
    removed_zips = 0
    errors = 0

    if not dry_run:
        for item in to_remove:
            item_path = os.path.join(output_root, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    removed_folders += 1
                else:
                    os.remove(item_path)
                    removed_zips += 1
            except Exception as e:
                print(f"Forge: Error pruning {item}: {e}")
                errors += 1

    return {
        "found": len(to_remove),
        "removed_folders": removed_folders,
        "removed_zips": removed_zips,
        "protected_count": len(protected),
        "errors": errors
    }

def sync_assets_to_project(output_root, target_path, name_filter=None, category_filter=None, dry_run=False):
    """
    Copies registry-referenced assets from Forge to an external project path.
    """
    registry_path = os.path.join(output_root, "registry.json")
    if not os.path.exists(registry_path):
        raise FileNotFoundError(f"Registry not found at {registry_path}. Sync requires a valid registry.")

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Could not read registry: {e}")

    assets = registry.get("assets", [])
    selected_assets = []
    
    for a in assets:
        if name_filter and a.get("name") != name_filter:
            continue
        if category_filter and a.get("category") != category_filter:
            continue
        selected_assets.append(a)

    if dry_run:
        print(f"\n--- SYNC DRY RUN to {target_path} ---")
        print(f"Assets selected: {len(selected_assets)}")

    folders_copied = 0
    zips_copied = 0
    warnings = 0
    errors = 0

    if not dry_run:
        os.makedirs(target_path, exist_ok=True)

    for a in selected_assets:
        pkg_rel = a.get("package_path")
        if pkg_rel:
            src_pkg = os.path.join(output_root, pkg_rel)
            dst_pkg = os.path.join(target_path, pkg_rel)
            if os.path.exists(src_pkg):
                if dry_run:
                    print(f" [SYNC] Folder: {pkg_rel}")
                else:
                    try:
                        if os.path.exists(dst_pkg):
                            shutil.rmtree(dst_pkg)
                        shutil.copytree(src_pkg, dst_pkg)
                        folders_copied += 1
                    except Exception as e:
                        print(f"Forge: Error copying folder {pkg_rel}: {e}")
                        errors += 1
            else:
                print(f"Forge: WARNING - Source folder missing: {src_pkg}")
                warnings += 1

        zip_rel = a.get("archive_path")
        if zip_rel:
            src_zip = os.path.join(output_root, zip_rel)
            dst_zip = os.path.join(target_path, zip_rel)
            if os.path.exists(src_zip):
                if dry_run:
                    print(f" [SYNC] ZIP:    {zip_rel}")
                else:
                    try:
                        shutil.copy2(src_zip, dst_zip)
                        zips_copied += 1
                    except Exception as e:
                        print(f"Forge: Error copying ZIP {zip_rel}: {e}")
                        errors += 1
            else:
                print(f"Forge: WARNING - Source ZIP missing: {src_zip}")
                warnings += 1

    return {
        "selected": len(selected_assets),
        "folders_copied": folders_copied,
        "zips_copied": zips_copied,
        "warnings": warnings,
        "errors": errors
    }

def get_library_list(output_root, category_filter=None, format_filter=None, sort_by="date"):
    """
    Returns a list of assets from registry.json with filtering and sorting.
    """
    registry_path = os.path.join(output_root, "registry.json")
    if not os.path.exists(registry_path):
        return []

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except Exception:
        return []

    assets = registry.get("assets", [])
    filtered = []
    for a in assets:
        if category_filter and a.get("category") != category_filter:
            continue
        if format_filter and a.get("format") != format_filter:
            continue
        filtered.append(a)
        
    # Sorting
    if sort_by == "name":
        filtered.sort(key=lambda x: x.get("name", "").lower())
    elif sort_by == "date":
        # Registry is usually appended to, but we ensure descending date (latest first)
        filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
    return filtered

def get_asset_info(output_root, asset_name):
    """
    Loads full manifest for a specific named asset in the registry.
    """
    registry_path = os.path.join(output_root, "registry.json")
    if not os.path.exists(registry_path):
        return None

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
    except Exception:
        return None

    # Find the latest matching asset name
    # We iterate backwards to find the most recent entry if logic allows duplicates
    target = None
    for a in reversed(registry.get("assets", [])):
        if a.get("name") == asset_name:
            target = a
            break
            
    if not target or not target.get("package_path"):
        return None

    manifest_path = os.path.join(output_root, target["package_path"], "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    return None
