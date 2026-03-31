import subprocess

def clone_repo(url: str, path: str):
    subprocess.run(["git", "clone", url, path])