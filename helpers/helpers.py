import json
import os

def get_project_root():
    """Retrieve the project root path from the configuration file."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "ifft_config.json")
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config.get("project_root", os.getcwd())

def resolve_path(relative_path):
    """Resolve a relative path to the project root."""
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)
