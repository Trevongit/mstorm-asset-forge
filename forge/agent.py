import re

def interpret_prompt(prompt):
    """
    Translates a natural language prompt into a deterministic forge request.
    Returns (dict request, str message) or (None, error_message).
    """
    if not prompt or not prompt.strip():
        return None, "Empty prompt provided."

    p = prompt.lower()
    
    # 1. Identify Primitive (Required)
    primitive = None
    if any(word in p for word in ["cube", "box", "square"]):
        primitive = "cube"
    elif any(word in p for word in ["sphere", "ball", "round"]):
        primitive = "sphere"
    elif any(word in p for word in ["cylinder", "pillar", "tube"]):
        primitive = "cylinder"
    elif any(word in p for word in ["plane", "floor", "ground", "flat"]):
        primitive = "plane"
        
    if not primitive:
        return None, f"Could not determine asset primitive from prompt: '{prompt}'"

    # 2. Identify Name (Guessed from keywords or generic)
    name = "nl_asset"
    # Simple heuristic: look for nouns that aren't the primitive
    if "table" in p: name = "table"
    elif "wall" in p: name = "wall"
    elif "pillar" in p: name = "pillar"
    elif "base" in p: name = "base"

    # 3. Identify Shading
    shading = "flat"
    if any(word in p for word in ["smooth", "polished", "soft"]):
        shading = "smooth"

    # 4. Identify Scale (Simple multiplier heuristics)
    scale = [1.0, 1.0, 1.0]
    if "tall" in p or "high" in p:
        scale = [1.0, 1.0, 3.0]
    elif "wide" in p or "broad" in p:
        scale = [3.0, 1.0, 1.0]
    elif "large" in p or "huge" in p:
        scale = [2.0, 2.0, 2.0]
    elif "small" in p or "tiny" in p:
        scale = [0.5, 0.5, 0.5]

    # Construct the request object
    request = {
        "asset": {
            "name": name,
            "primitive": primitive,
            "scale": scale
        },
        "options": {
            "shading": shading,
            "tags": ["nl_interpreted", "agent_skeleton"]
        }
    }
    
    return request, f"Interpreted '{prompt}' as {primitive} ({shading})"
