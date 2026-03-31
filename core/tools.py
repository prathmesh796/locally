import os
from langchain.tools import tool
from services.executor import execute_command

@tool
def run_shell_command(command: str, cwd: str) -> str:
    """
    Executes a shell command in the specified directory (cwd) and returns its output.
    Useful for installing dependencies, running the app, or fixing environments.
    """
    res = execute_command(command, cwd)
    output = f"Status: {res['status']}\nExit code: {res['return_code']}\n"
    if res['stdout']:
        output += f"STDOUT:\n{res['stdout']}\n"
    if res['stderr']:
        output += f"STDERR:\n{res['stderr']}\n"
    return output

@tool
def read_file(file_path: str) -> str:
    """Reads the contents of a file."""
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

@tool
def list_dir(directory: str) -> str:
    """Lists files and directories in the specified directory."""
    if not os.path.exists(directory):
        return f"Error: Directory '{directory}' does not exist."
    try:
        items = os.listdir(directory)
        return "\n".join(items) if items else "Directory is empty."
    except Exception as e:
        return f"Error listing directory '{directory}': {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Useful for creating .env files or fixing configs."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' written successfully."
    except Exception as e:
        return f"Error writing file '{file_path}': {str(e)}"
