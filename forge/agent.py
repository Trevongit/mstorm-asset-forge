import re

def interpret_prompt(prompt):
    """
    Translates a natural language prompt into a deterministic forge request.
    Returns (dict request, str message) or (None, error_message).
    """
    if not prompt or not prompt.strip():
        return None, "Empty prompt provided."

    p = prompt.lower()
    
    # 0. Unsupported Concept Check (Hard Fail)
    unsupported = ["donut", "torus", "cone", "monkey", "suzanne", "light", "camera"]
    for word in unsupported:
        if word in p:
            return None, f"Unsupported concept detected: '{word}'. The MVP only supports basic primitives."

    # 1. Identify Primitive (Required)
    primitive = None
    if any(word in p for word in ["cube", "box", "square"]):
        primitive = "cube"
    elif any(word in p for word in ["sphere", "ball", "round"]):
        primitive = "sphere"
    elif any(word in p for word in ["cylinder", "pillar", "tube"]):
        primitive = "cylinder"
    elif any(word in p for word in ["plane", "floor", "ground", "flat", "sheet", "wall"]):
        primitive = "plane"
        
    if not primitive:
        return None, f"Could not determine asset primitive from prompt: '{prompt}'"

    # 2. Improved Name Inference
    # Strip known keywords and articles to find the "subject"
    noise = [
        "a", "an", "the", "make", "create", "generate", "build", "simple",
        "cube", "box", "square", "sphere", "ball", "round", "cylinder", "pillar", "tube", "plane", "floor", "ground", "flat", "sheet", "wall",
        "smooth", "polished", "soft", "matte", "rough",
        "tall", "high", "wide", "broad", "large", "huge", "small", "tiny", "thin", "pancake", "skinny", "needle"
    ]
    
    # Replace noise with spaces, then collapse
    name_candidate = p
    for word in noise:
        name_candidate = re.sub(rf'\b{word}\b', '', name_candidate)
    
    name_clean = "_".join(re.findall(r'\w+', name_candidate))
    name = name_clean if name_clean else f"{primitive}_prop"

    # 3. Identify Shading
    shading = "flat"
    if any(word in p for word in ["smooth", "polished", "soft"]):
        shading = "smooth"
    elif any(word in p for word in ["matte", "rough", "flat"]):
        shading = "flat"

    # 4. Expanded Scale Mappings
    scale = [1.0, 1.0, 1.0]
    if "tall" in p or "high" in p:
        scale = [1.0, 1.0, 3.0]
    elif "wide" in p or "broad" in p:
        scale = [3.0, 1.0, 1.0]
    elif "large" in p or "huge" in p:
        scale = [2.0, 2.0, 2.0]
    elif "small" in p or "tiny" in p:
        scale = [0.5, 0.5, 0.5]
    elif "thin" in p or "pancake" in p or "flat" in p:
        scale = [1.0, 1.0, 0.1]
    elif "skinny" in p or "needle" in p:
        scale = [0.1, 0.1, 2.0]

    # Construct the request object
    request = {
        "asset": {
            "name": name,
            "primitive": primitive,
            "scale": scale
        },
        "options": {
            "shading": shading,
            "tags": ["nl_interpreted", "agent_v0.2"]
        }
    }
    
    return request, f"Interpreted '{prompt}' as {primitive} ({shading})"
