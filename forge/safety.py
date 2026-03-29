import re

def validate_snippet(code: str) -> tuple[bool, str]:
    """
    Validates a bpy snippet against a very narrow safety model.
    Focuses strictly on geometry creation.
    """
    if not code or not code.strip():
        return False, "Snippet is empty."

    # 1. Strict Blacklist
    forbidden_patterns = [
        r"\bimport\b", r"\bfrom\b", r"\bopen\(", r"\bread\(", r"\bwrite\(",
        r"\bexec\b", r"\beval\b", r"\bcompile\b", r"__",
        r"\bdef\b", r"\bclass\b", r"\bos\.", r"\bsys\.",
        r"subprocess", r"socket", r"requests", r"pathlib", r"urllib",
        r"bpy\.ops\.wm", r"bpy\.ops\.render", r"bpy\.ops\.export",
        r"bpy\.context\.preferences",
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, code):
            return False, f"Forbidden pattern detected: '{pattern}'"

    # 2. Strict Geometry-Only Expectation
    # For this slice, we REQUIRE the use of bpy.ops.mesh operators
    if "bpy.ops.mesh." not in code:
        return False, "Snippet must use 'bpy.ops.mesh.*' for geometry creation."

    return True, ""
