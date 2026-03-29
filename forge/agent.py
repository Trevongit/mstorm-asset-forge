import re
import json
from .llm_connector import get_connector

def interpret_prompt_rule_based(prompt):
    """
    Translates a natural language prompt into a deterministic forge request
    using local keyword heuristics.
    """
    if not prompt or not prompt.strip():
        return None, "Empty prompt provided."

    p = prompt.lower()
    
    # 0. Unsupported Concept Check
    unsupported = ["donut", "torus", "cone", "monkey", "suzanne", "light", "camera"]
    for word in unsupported:
        if word in p:
            return None, f"Unsupported concept detected: '{word}'. The MVP only supports basic primitives."

    # 1. Identify Primitive
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
    noise = [
        "a", "an", "the", "make", "create", "generate", "build", "simple",
        "cube", "box", "square", "sphere", "ball", "round", "cylinder", "pillar", "tube", "plane", "floor", "ground", "flat", "sheet", "wall",
        "smooth", "polished", "soft", "matte", "rough",
        "tall", "high", "wide", "broad", "large", "huge", "small", "tiny", "thin", "pancake", "skinny", "needle"
    ]
    name_candidate = p
    for word in noise:
        name_candidate = re.sub(rf'\b{word}\b', '', name_candidate)
    
    name_clean = "_".join(re.findall(r'\w+', name_candidate))
    name = name_clean if name_clean else f"{primitive}_prop"

    # 3. Identify Shading
    shading = "flat"
    if any(word in p for word in ["smooth", "polished", "soft"]):
        shading = "smooth"

    # 4. Scale Mappings
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

    request = {
        "asset": {
            "name": name,
            "primitive": primitive,
            "scale": scale
        },
        "options": {
            "shading": shading,
            "tags": ["nl_interpreted", "rule_based"]
        }
    }
    
    return request, f"Rule-based success: {primitive} ({shading})"

def interpret_prompt(prompt, use_llm=False, provider="openai", model=None, sandbox_mode=False, batch_mode=False):
    """
    Main entry point for prompt interpretation.
    Routes to either rule-based or LLM-based logic.
    """
    if not use_llm:
        if sandbox_mode or batch_mode:
            mode_name = "Sandbox" if sandbox_mode else "Batch"
            return None, f"Experimental mode ({mode_name}) requires --llm."
        return interpret_prompt_rule_based(prompt)
    
    try:
        connector = get_connector(provider, model)
        result = connector.generate_request(prompt, sandbox_mode=sandbox_mode, batch_mode=batch_mode)
        
        # Validation and normalization for both Single and Batch results
        items = result if isinstance(result, list) else [result]
        
        if not items:
            return None, "LLM returned an empty list of requests."

        for item in items:
            if "asset" not in item:
                return None, "LLM returned invalid structure (missing 'asset' key)."
            
            # Ensure tags indicate LLM provenance
            if "options" not in item:
                item["options"] = {}
            if "tags" not in item["options"]:
                item["options"]["tags"] = []
            
            # Deduplicate provenance tags
            prov_tags = ["llm_interpreted", f"provider_{provider}"]
            for t in prov_tags:
                if t not in item["options"]["tags"]:
                    item["options"]["tags"].append(t)
        
        # Return list if batch mode requested, else single dict
        return (items if batch_mode else items[0]), f"LLM ({provider}) success."
    except Exception as e:
        return None, f"LLM Error: {e}"
