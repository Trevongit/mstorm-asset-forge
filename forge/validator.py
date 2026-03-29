import os

VALIDATION_PROFILES = {
    "mobile": {
        "max_face_count": 10000,
        "max_file_size_mb": 10,
        "preferred_format": "glb"
    },
    "standard": {
        "max_face_count": 50000,
        "max_file_size_mb": 50,
        "preferred_format": None
    },
    "high_fidelity": {
        "max_face_count": 250000,
        "max_file_size_mb": 250,
        "preferred_format": None
    }
}

def validate_asset(package_path, asset_params, options, geometry_stats=None):
    """
    Validates the generated asset artifacts against a profile.
    Returns (bool success, list errors, list warnings, dict validation_meta)
    """
    errors = []
    warnings = []
    meta = {}
    
    # Resolve Profile
    profile_name = options.get("validation_profile", "standard")
    if profile_name not in VALIDATION_PROFILES:
        warnings.append(f"Unknown validation profile '{profile_name}', falling back to 'standard'")
        profile_name = "standard"
    
    profile = VALIDATION_PROFILES[profile_name]
    meta["validation_profile"] = profile_name
    
    fmt = options.get("format", "obj")
    entry_point_name = f"asset.{fmt}"
    entry_point_path = os.path.join(package_path, entry_point_name)
    
    # --- 1. Hard Failure Checks (Global) ---
    
    # Check entry point existence
    if not os.path.exists(entry_point_path):
        errors.append(f"Entry point file missing: {entry_point_name}")
    else:
        size = os.path.getsize(entry_point_path)
        meta["file_size_bytes"] = size
        if size == 0:
            errors.append(f"Entry point file is empty: {entry_point_name}")
            
    # Check format consistency
    if os.path.exists(entry_point_path):
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

    # --- 2. Profile-Based Warning/Error Checks ---
    
    # Face count check
    if geometry_stats:
        faces = geometry_stats.get("face_count", 0)
        meta["face_count"] = faces
        max_faces = profile["max_face_count"]
        if faces > max_faces:
            # For now, keep as warning but clearly state profile limit
            warnings.append(f"[{profile_name}] High poly count: {faces} faces (limit: {max_faces})")
            
    # File size check
    if "file_size_bytes" in meta:
        mb_size = meta["file_size_bytes"] / (1024 * 1024)
        max_mb = profile["max_file_size_mb"]
        if mb_size > max_mb:
            warnings.append(f"[{profile_name}] Large file size: {mb_size:.2f} MB (limit: {max_mb} MB)")

    # Format preference check
    pref_fmt = profile.get("preferred_format")
    if pref_fmt and fmt.lower() != pref_fmt.lower():
        warnings.append(f"[{profile_name}] Format '{fmt}' is non-standard; '{pref_fmt}' is preferred")

    # Missing preview check
    preview_path = os.path.join(package_path, "preview.png")
    if not os.path.exists(preview_path) and not options.get("no_preview"):
        warnings.append("Preview image missing")

    # Final status
    success = len(errors) == 0
    
    return success, errors, warnings, meta
