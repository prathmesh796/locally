import subprocess

def install_dependencies(path: str, project_type: str):
    if project_type == "node":
        subprocess.run(["npm", "install"], cwd=path)
    elif project_type == "python":
        subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=path)