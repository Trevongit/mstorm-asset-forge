"""
Configuration loader for MStorm Asset Forge.
"""

import os
import yaml
from pathlib import Path

def load_config(config_path=None):
    """
    Load configuration from a YAML file and environment variables.
    """
    if config_path is None:
        # Default config path
        repo_root = Path(__file__).parent.parent.absolute()
        config_path = repo_root / "config" / "config.yaml"
    
    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    
    # Environment variable overrides
    # (Using ASSET_FORGE_ prefix for new vars)
    if os.environ.get("ASSET_FORGE_OUTPUT_DIR"):
        config.setdefault("storage", {})["output_dir"] = os.environ.get("ASSET_FORGE_OUTPUT_DIR")
        
    return config
