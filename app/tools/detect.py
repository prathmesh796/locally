import os

def detect_project_type(path: str):
    if os.path.exists(f"{path}/package.json"):
        return "node"
    elif os.path.exists(f"{path}/requirements.txt"):
        return "python"
    return "unknown"