import os

def validate_asset(package_path, asset_params, options, geometry_stats=None):
    """
    Validates the generated asset artifacts.
    Returns (bool success, list errors, list warnings, dict validation_meta)
    """
    errors = []
    warnings = []
    meta = {}
    
    fmt = options.get("format", "obj")
    entry_point_name = f"asset.{fmt}"
    entry_point_path = os.path.join(package_path, entry_point_name)
    
    # --- 1. Hard Failure Checks ---
    
    # Check entry point existence
    if not os.path.exists(entry_point_path):
        errors.append(f"Entry point file missing: {entry_point_name}")
    else:
        size = os.path.getsize(entry_point_path)
        meta["file_size_bytes"] = size
        if size == 0:
            errors.append(f"Entry point file is empty: {entry_point_name}")
            
    # Check format consistency
    # (Already checked by path existence above, but explicit)
    ext = os.path.splitext(entry_point_path)[1].lower().strip('.')
    if ext != fmt.lower():
        errors.append(f"Format mismatch: expected {fmt}, found {ext}")

    # Check zip if requested
    if options.get("zip"):
        zip_name = f"{os.path.basename(package_path)}.zip"
        zip_path = os.path.join(os.path.dirname(package_path), zip_name)
        if not os.path.exists(zip_path):
            errors.append(f"Requested ZIP archive missing: {zip_name}")
        else:
            meta["zip_size_bytes"] = os.path.getsize(zip_path)

    # --- 2. Warning Checks ---
    
    # High poly count check
    if geometry_stats:
        faces = geometry_stats.get("face_count", 0)
        meta["face_count"] = faces
        if faces > 50000:
            warnings.append(f"High poly count: {faces} faces")
            
    # Large file size check
    if "file_size_bytes" in meta:
        mb_size = meta["file_size_bytes"] / (1024 * 1024)
        if mb_size > 50:
            warnings.append(f"Large file size: {mb_size:.2f} MB")

    # Missing preview check
    preview_path = os.path.join(package_path, "preview.png")
    if not os.path.exists(preview_path) and not options.get("no_preview"):
        warnings.append("Preview image missing")

    # Final status
    success = len(errors) == 0
    
    return success, errors, warnings, meta
