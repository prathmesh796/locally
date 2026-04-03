import subprocess
from typing import Dict, Any
from app.utils.logger import logger, console

def execute_command(command: str, cwd: str, timeout: int = 60) -> Dict[str, Any]:
    """Execute a shell command and return its output. Includes a timeout for long-running processes."""
    logger.info(f"Executing: `{command}` in {cwd} with timeout {timeout}s")
    console.print(f"[dim]Running:[/dim] {command}")
    
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout
        )
        return {
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "status": "completed"
        }
    except subprocess.TimeoutExpired as e:
        logger.warning(f"Execution timed out after {timeout} seconds.")
        # If it times out, it might be a successfully running server like Next.js
        return {
            "command": command,
            "return_code": 0,
            "stdout": e.stdout if e.stdout is not None else "Process is still running (Timeout reached). Likely a server started successfully.",
            "stderr": e.stderr if e.stderr is not None else "",
            "status": "timeout"
        }
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "status": "error"
        }
